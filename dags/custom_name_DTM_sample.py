from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def process_data(data):
    # Perform data processing logic here
    print(f"Processing data: {data}")

@dag(
    dag_id="custom_task_mapping_example",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
)
def custom_task_mapping_example():
    mapped_processes = PythonOperator.partial(
        task_id="process_data_source",
        python_callable=process_data,
        map_index_template="Processing source={{ task.op_args[0] }}",
    ).expand(op_args=[["source_a"], ["source_b"], ["source_c"]])

custom_task_mapping_example()
