# API to S3 to Snowflake ETL Pipeline

This project demonstrates a real-world, production-style ETL pipeline that:

- Extracts data from a public API
- Validates it using [Great Expectations](https://greatexpectations.io/)
- Uploads the data to an AWS S3 bucket
- Loads the validated data into a Snowflake data warehouse
- Orchestrates everything using Apache Airflow
- Logs progress and sends email alerts on failure

---

## 📦 Project Structure

```
.
├── your_etl_module.py                # ETL logic: extract, transform, load
├── great_expectations_validation.py # Data quality checks using Great Expectations
├── api_to_s3_to_snowflake_dag.py    # Airflow DAG definition
└── README.md                         # Project overview (this file)
```

---

## 🛠 Tech Stack

- **Python**
- **Airflow**
- **AWS S3** (via `boto3`)
- **Snowflake** (via `snowflake-connector-python`)
- **Great Expectations**
- **SMTP Email Alerts**

---

## 🚀 How to Run

1. Set up your environment:
   - Airflow environment
   - AWS credentials (`~/.aws/credentials` or Airflow connections)
   - Snowflake account and table
   - Great Expectations initialized in `/opt/airflow/great_expectations`

2. Customize:
   - Replace credentials and table names in `your_etl_module.py`
   - Set your email for alerts in the DAG file
   - Adjust S3 bucket and file paths

3. Deploy the DAG:
   - Copy `api_to_s3_to_snowflake_dag.py` into your Airflow `dags/` folder
   - Start the Airflow scheduler & webserver

---

## ✅ Features

- Logging at every step
- Email alerts on failure (SMTP setup in Airflow required)
- Data validation step before S3 upload
- Snowflake `COPY INTO` for ingestion
- Modular and production-ready Python code

---

## 📧 Alerts Setup

Ensure you configure `airflow.cfg` with your SMTP details under the `[smtp]` section:

```
[smtp]
smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = your.email@gmail.com
smtp_password = your_app_password
smtp_port = 587
smtp_mail_from = airflow@example.com
```

---

## 👀 Sample API Used

[JSONPlaceholder](https://jsonplaceholder.typicode.com/users) – a free fake REST API for testing and prototyping.

---

## 📎 License

License — free to use and modify.
