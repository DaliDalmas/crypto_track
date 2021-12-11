import airflow
from airflow import DAG 
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python import task
from airflow.operators.python_operator import PythonOperator

from tasks.download_todays_crypto import get_data
# Instantiate a DAG object; this is the starting point of any workflow.
dag = DAG(
   dag_id="get_todays_crypto",   # Name of the DAG
   start_date=airflow.utils.dates.days_ago(1),  # The date at which the DAG should first start running
   schedule_interval=None,  # We will manually trigger the DAG
)

run_download_todays_crypto = PythonOperator(
    task_id = 'run_download_todays_crypto',
    python_callable = get_data,
    dag=dag
)

# Set the order of execution of tasks.
run_download_todays_crypto