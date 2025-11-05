from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# --- Add project root to path so the 'db' package can be imported ---
# If this file is at <project>/airflow/dags/etl_pipeline.py then PROJECT_ROOT should be <project>
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# also ensure db folder is importable if it's a top-level package directory
DB_PATH = os.path.join(PROJECT_ROOT, "db")
if DB_PATH not in sys.path:
    sys.path.append(DB_PATH)

# Import your db scripts
from db.init_schema import create_schema as init_schema
from db.fetch_and_insert import insert_data
from db.transformations import transform_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="flight_etl_pipeline",
    default_args=default_args,
    description="Daily ETL for Flight Sales Data",
    schedule_interval="0 0 * * *",  # every day at 00:00
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=["flight", "etl", "duckdb"],
) as dag:

    init_schema_task = PythonOperator(
        task_id="init_schema",
        python_callable=init_schema,
    )

    fetch_insert_task = PythonOperator(
        task_id="fetch_and_insert",
        python_callable=insert_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    # Task dependencies
    init_schema_task >> fetch_insert_task >> transform_task

# What it does: This DAG initializes the DuckDB schema, fetches flight sales data from an API,
# and transforms it for analysis.