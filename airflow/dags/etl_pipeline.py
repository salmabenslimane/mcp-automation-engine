from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# --- Add airflow root folder (/opt/airflow) to sys.path ---
AIRFLOW_HOME = os.path.dirname(os.path.dirname(__file__))  # /opt/airflow
if AIRFLOW_HOME not in sys.path:
    sys.path.append(AIRFLOW_HOME)

# ✅ Import from airflow/db
from db.db_connection import get_connection
from db.init_schema import create_schema as init_schema
from db.fetch_and_insert import insert_data
from db.transformations import transform_data

# --------------------------
# DAG DEFINITION
# --------------------------
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
    schedule="0 0 * * *",  # every day at midnight
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
