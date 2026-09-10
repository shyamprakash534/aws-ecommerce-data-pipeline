# AWS E-Commerce Data Pipeline

Portfolio project demonstrating an AWS-style e-commerce analytics pipeline with a Streamlit business output layer.

## Architecture
Raw S3 → AWS Glue → Curated S3 → Athena → Dashboard

The repository includes validated local output datasets for monthly sales, category performance and late-delivery analysis. The dashboard also supports CSV upload for interactive analysis.

## Features
- CSV input and validation
- Revenue, order volume and AOV KPIs
- Revenue trend analysis
- Category revenue analysis
- Late-delivery analysis
- Pipeline architecture view
- Downloadable processed output

## Stack
Python, Pandas, Plotly, Streamlit, AWS S3, AWS Glue, Amazon Athena

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

> Note: the Streamlit application is the portfolio-facing analytics layer. AWS infrastructure should only be described as provisioned when separately deployed and verified.