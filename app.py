from pathlib import Path
import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AWS E-Commerce Data Pipeline", page_icon="☁️", layout="wide", initial_sidebar_state="expanded")
BASE=Path(__file__).parent; OUT=BASE/"data"/"local_output"
@st.cache_data
def load_default_data():
    return pd.read_csv(OUT/"monthly_sales.csv"),pd.read_csv(OUT/"top_categories.csv"),pd.read_csv(OUT/"late_delivery_rate.csv")
def process_upload(file):
    df=pd.read_csv(file); cols={c.lower().strip().replace(" ","_"):c for c in df.columns}
    if "order_year_month" in cols and "total_revenue" in cols:
        m=df.rename(columns={cols["order_year_month"]:"order_year_month",cols["total_revenue"]:"total_revenue"})
        if "num_orders" not in m:m["num_orders"]=1
        if "avg_order_value" not in m:m["avg_order_value"]=m["total_revenue"]/m["num_orders"].replace(0,1)
        return m,pd.DataFrame(columns=["product_category","total_revenue","num_orders"]),pd.DataFrame(columns=["order_year_month","delivered_orders","late_pct"])
    raise ValueError("CSV needs at least order_year_month and total_revenue columns.")
monthly,cats,late=load_default_data()
st.markdown("""<style>[data-testid="stAppViewContainer"]{background:#f6f7fb}.block-container{max-width:1450px;padding:1.8rem 2.5rem 3rem}[data-testid="stSidebar"]{border-right:1px solid #e6e8ef}.hero{background:linear-gradient(120deg,#111827,#243b64);padding:28px 32px;border-radius:20px;color:#fff;margin-bottom:20px}.hero h1{font-size:30px;margin:0;font-weight:750}.hero p{margin:7px 0 0;color:#d9e2f2;font-size:14px}.card{background:#fff;border:1px solid #e6e8ef;border-radius:16px;padding:18px 20px;min-height:105px;box-shadow:0 2px 10px rgba(16,24,40,.04)}.label{font-size:12px;color:#667085;font-weight:600}.value{font-size:25px;color:#101828;font-weight:750;margin-top:7px}.muted{font-size:12px;color:#98a2b3;margin-top:4px}.section{font-size:20px;font-weight:700;color:#101828;margin:24px 0 12px}</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>AWS E-Commerce Data Pipeline</h1><p>Upload data, validate it, and turn processed outputs into decision-ready business insights.</p></div>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown("### INPUTS"); uploaded=st.file_uploader("Upload CSV",type=["csv"])
    if uploaded:
        try:
            monthly,uc,ul=process_upload(io.BytesIO(uploaded.getvalue()));
            if not uc.empty:cats=uc
            if not ul.empty:late=ul
            st.success("Data loaded")
        except Exception as e:st.error(str(e))
    metric=st.selectbox("Output metric",["total_revenue","num_orders","avg_order_value"],format_func=lambda x:{"total_revenue":"Revenue","num_orders":"Orders","avg_order_value":"Average Order Value"}[x]); show_unknown=st.checkbox("Include unknown category",False)
monthly["month"]=pd.to_datetime(monthly["order_year_month"]); revenue=pd.to_numeric(monthly["total_revenue"],errors="coerce").sum(); orders=pd.to_numeric(monthly["num_orders"],errors="coerce").sum(); aov=revenue/orders if orders else 0; late_rate=pd.to_numeric(late["late_pct"],errors="coerce").mean() if not late.empty else 0
c=st.columns(4)
for col,label,value,sub in [(c[0],"TOTAL REVENUE",f"${revenue:,.2f}","Processed output"),(c[1],"TOTAL ORDERS",f"{orders:,.0f}","Validated order volume"),(c[2],"AVG ORDER VALUE",f"${aov:,.2f}","Revenue ÷ orders"),(c[3],"LATE DELIVERY",f"{late_rate:.2f}%","Average monthly rate")]:col.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="muted">{sub}</div></div>',unsafe_allow_html=True)
st.markdown('<div class="section">OUTPUTS</div>',unsafe_allow_html=True); t1,t2,t3=st.tabs(["Trend","Categories","Delivery"])
with t1:
    title={"total_revenue":"Revenue Trend","num_orders":"Order Volume Trend","avg_order_value":"Average Order Value Trend"}[metric]; fig=px.line(monthly.sort_values("month"),x="month",y=metric,markers=True,title=title); fig.update_layout(height=410,margin=dict(l=10,r=10,t=55,b=10),hovermode="x unified",plot_bgcolor="white",paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True); st.dataframe(monthly.drop(columns=["month"],errors="ignore"),use_container_width=True,hide_index=True); st.download_button("Download output CSV",monthly.drop(columns=["month"],errors="ignore").to_csv(index=False),"monthly_output.csv","text/csv")
with t2:
    v=cats.copy();
    if not show_unknown and "product_category" in v:v=v[v.product_category.str.lower()!="unknown"]
    if v.empty:st.info("Category output is not available for the uploaded CSV.")
    else:st.plotly_chart(px.bar(v.sort_values("total_revenue"),x="total_revenue",y="product_category",orientation="h",title="Revenue by Category",text_auto=".2s"),use_container_width=True); st.dataframe(v,use_container_width=True,hide_index=True)
with t3:
    if late.empty:st.info("Delivery output is not available for the uploaded CSV.")
    else:
        late["month"]=pd.to_datetime(late.order_year_month); st.plotly_chart(px.line(late.sort_values("month"),x="month",y="late_pct",markers=True,title="Late Delivery Rate"),use_container_width=True); st.dataframe(late.drop(columns=["month"],errors="ignore"),use_container_width=True,hide_index=True)
st.markdown('<div class="section">PIPELINE</div>',unsafe_allow_html=True); flow=st.columns(5)
for col,title,desc in zip(flow,["Raw S3","AWS Glue","Curated S3","Athena","Dashboard"],["Input data","Transform + quality","Analytics data","SQL queries","Business output"]):col.markdown(f'<div class="card"><b>{title}</b><br><span class="muted">{desc}</span></div>',unsafe_allow_html=True)
st.caption("Input → Processing → Output. The repository contains validated local output datasets; the dashboard supports CSV upload for interactive analysis.")