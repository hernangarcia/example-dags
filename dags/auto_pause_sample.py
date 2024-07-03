from airflow.decorators import dag, task
from datetime import datetime, timedelta

@task
def failing_task():
    raise ValueError("This task is designed to fail")

@dag(
    dag_id="auto_pause",
    start_date=datetime(2023, 1, 1),
    schedule_interval=timedelta(minutes=1),  # Run every minute
    catchup=False,
    max_consecutive_failed_dag_runs=3,  # Set the maximum number of consecutive failed DAG runs
)
def example_dag_with_auto_pause():
    failing_task_instance = failing_task()

example_dag_with_auto_pause()
