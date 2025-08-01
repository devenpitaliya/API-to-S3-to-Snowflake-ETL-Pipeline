
import requests
import pandas as pd
import boto3
import snowflake.connector
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

def extract_data():
    logger.info("Extracting data from API...")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    logger.info(f"Extracted {len(df)} records.")
    return df

def save_to_csv(df, filepath):
    logger.info(f"Saving data to CSV at {filepath}...")
    df.to_csv(filepath, index=False)
    logger.info("CSV saved.")

def upload_to_s3(local_file, bucket, s3_key):
    logger.info(f"Uploading {local_file} to s3://{bucket}/{s3_key} ...")
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket, s3_key)
    logger.info("Upload to S3 complete.")

def load_to_snowflake(s3_bucket, s3_key, table_name):
    logger.info(f"Loading data from s3://{s3_bucket}/{s3_key} into Snowflake table {table_name}...")
    conn = snowflake.connector.connect(
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='YOUR_WAREHOUSE',
        database='YOUR_DATABASE',
        schema='YOUR_SCHEMA',
        role='YOUR_ROLE'
    )
    cursor = conn.cursor()
    copy_query = f"""
        COPY INTO {table_name}
        FROM 's3://{s3_bucket}/{s3_key}'
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
        PATTERN = '.*\\.csv'
        ON_ERROR = 'CONTINUE'
    """
    cursor.execute(copy_query)
    cursor.close()
    conn.close()
    logger.info("Snowflake load complete.")
