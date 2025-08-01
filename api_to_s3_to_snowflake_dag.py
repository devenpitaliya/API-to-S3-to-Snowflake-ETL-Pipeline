
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from your_etl_module import extract_data, save_to_csv, upload_to_s3, load_to_snowflake
from great_expectations_validation import validate_data_with_ge

default_args = {
    'owner': 'airflow',
    'email': ['your.email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='api_to_s3_to_snowflake',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'api', 's3', 'snowflake']
) as dag:

    def extract_and_save():
        df = extract_data()
        save_to_csv(df, '/tmp/users.csv')

    extract = PythonOperator(
        task_id='extract_api',
        python_callable=extract_and_save
    )

    validate = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_with_ge
    )

    upload = PythonOperator(
        task_id='upload_to_s3',
        python_callable=lambda: upload_to_s3('/tmp/users.csv', 'your-bucket-name', 'etl/users.csv')
    )

    load = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=lambda: load_to_snowflake('your-bucket-name', 'etl/users.csv', 'USERS')
    )

    extract >> validate >> upload >> load
