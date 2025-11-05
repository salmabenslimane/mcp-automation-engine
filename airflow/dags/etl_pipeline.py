from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import os

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

# Define your DAG
with DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='ETL pipeline to load and process flight sales data using DuckDB',
    schedule='@daily',
    start_date=datetime(2025, 11, 1),
    catchup=False,
    tags=['duckdb', 'etl', 'flight-sales'],
) as dag:

    def run_init_schema():
        """Create the DuckDB schema if it doesn't exist."""
        script_path = "/opt/airflow/db/init_schema.py"
        print(f"Running {script_path} ...")
        subprocess.run(["python", script_path], check=True)
        print("✅ Schema initialized successfully.")

    def run_fetch_and_insert():
        """Fetch data from API and insert into DuckDB."""
        script_path = "/opt/airflow/db/fetch_and_insert.py"
        print(f"Running {script_path} ...")
        subprocess.run(["python", script_path], check=True)
        print("✅ Data fetched and inserted successfully.")

    # Define tasks
    init_schema = PythonOperator(
        task_id='init_schema',
        python_callable=run_init_schema,
    )

    fetch_and_insert = PythonOperator(
        task_id='fetch_and_insert',
        python_callable=run_fetch_and_insert,
    )

    # DAG dependencies
    init_schema >> fetch_and_insert
