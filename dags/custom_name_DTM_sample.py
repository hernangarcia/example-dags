from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def process_data(data):
    # Perform data processing logic here
    print(f"Processing data: {data}")

with DAG(
    dag_id="custom_task_mapping_example",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    data_sources = ["source_a", "source_b", "source_c"]

    mapped_task = PythonOperator.partial(
        task_id="process_data",
        python_callable=process_data,
        map_index_template="{{ task.env['SOURCE'] }}",  # Custom naming template
    ).expand(
        env=[{"SOURCE": source} for source in data_sources]  # Data sources
    )