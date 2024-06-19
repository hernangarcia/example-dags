from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def failing_task():
    raise ValueError("This task is designed to fail")

with DAG(
    dag_id="example_dag_with_auto_pause",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    max_consecutive_failed_dag_runs=3,  # Set the maximum number of consecutive failed DAG runs
) as dag:

    task = PythonOperator(
        task_id="failing_task",
        python_callable=failing_task,
    )
