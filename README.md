# AWS E-Commerce Data Pipeline

Portfolio project demonstrating an AWS-style e-commerce analytics pipeline with a Streamlit business output layer.

The project focuses on the **data flow and analytics experience**: raw e-commerce data is validated, transformed into curated outputs, queried conceptually through an AWS analytics stack, and surfaced through a dashboard.

> **Scope note:** This repository is a portfolio implementation. The README does not claim that the AWS infrastructure below is currently provisioned in a live AWS account. Describe AWS resources as deployed only when they have been separately provisioned and verified.

## Live Application

**https://aws-ecommerce-data-pipeline.onrender.com**

The live Streamlit application provides the portfolio-facing analytics experience. The AWS architecture shown below represents the intended cloud pipeline design.

## Architecture

```text
Raw E-Commerce Data
        |
        v
   Amazon S3
        |
        v
   AWS Glue
   (ETL / validation)
        |
        v
  Curated S3 Data
        |
        v
   Amazon Athena
        |
        v
   Analytics Layer
        |
        v
 Streamlit Dashboard
```

The repository also includes validated local output datasets for monthly sales, category performance and late-delivery analysis. The dashboard supports CSV upload for interactive analysis.

## What It Demonstrates

- Designing an analytics pipeline from raw data to business-facing output
- Data validation and transformation
- KPI-oriented analytics
- Separation between data processing and dashboard presentation
- AWS service mapping for object storage, ETL and SQL analytics
- Reproducible local execution without requiring an AWS account

## Dashboard Features

- Executive-style KPI view
- Revenue and order-volume trends
- Average order value (AOV)
- Category revenue analysis
- Late-delivery analysis
- Pipeline architecture view
- Downloadable processed output
- CSV input and validation

## Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| Data processing | Pandas |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Cloud architecture | Amazon S3, AWS Glue, Amazon Athena |

## Run Locally

```bash
git clone https://github.com/shyamprakash534/aws-ecommerce-data-pipeline.git
cd aws-ecommerce-data-pipeline

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Project Boundaries

This project intentionally separates **architecture design** from **verified infrastructure deployment**.

- The dashboard is a runnable application.
- The AWS S3 → Glue → curated S3 → Athena flow describes the intended cloud architecture.
- No live AWS infrastructure should be inferred from the architecture diagram alone.
- Deployment claims should be updated only after the corresponding AWS resources are provisioned and verified.

This keeps the portfolio description reproducible and avoids presenting a design exercise as production infrastructure.

## Engineering Trade-offs

### Cloud architecture vs local reproducibility
The AWS services provide a realistic cloud data-platform model, while local execution keeps the project easy to review without requiring AWS credentials or paid infrastructure.

### Dashboard simplicity vs production BI
Streamlit keeps the business output layer lightweight and easy to demonstrate. A production analytics platform could use a dedicated BI service and governed semantic layer.

### Synthetic/local data vs sensitive production data
The project can be demonstrated without exposing real customer information. Production adoption would require stronger data governance, access controls, monitoring and retention policies.

## Limitations

- The current public deployment is the dashboard layer rather than a verified end-to-end AWS production pipeline.
- Performance and cost characteristics of a real S3/Glue/Athena deployment are not established by the local application.
- The repository does not claim production-grade data governance or SLA guarantees.

## Author

**Shyam Prakash**

- GitHub: https://github.com/shyamprakash534
- LinkedIn: https://www.linkedin.com/in/shyam-prakash-vemula-721029263
