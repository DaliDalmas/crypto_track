import json
import pathlib
import airflow
import requests
import requests.exceptions as requests_exceptions 
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.email_operator import EmailOperator

# Instantiate a DAG object; this is the starting point of any workflow.
dag = DAG(
   dag_id="vaccine_details",   # Name of the DAG
   start_date=airflow.utils.dates.days_ago(2),  # The date at which the DAG should first start running
   schedule_interval=None,  # We will manually trigger the DAG
)

# Creating first task
download_vaccine_details = BashOperator(
   task_id="download_vaccine_details", #Name of the task
   #Curl request to fetch the vaccine details from the API exposed by the government and store the results in vaccine.json file.
   bash_command="curl -X GET 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=110001&date=16-05-2021' -H  'accept: application/json' | jq >> /tmp/vaccine.json",
   dag=dag, #Reference to the DAG variable
)

#Creating second task
notify_user = BashOperator(
   task_id="notify_user",
   # Print the file content in the task log 
   bash_command='cat /tmp/vaccine.json',
   dag=dag,
)

#Creating third task
email = EmailOperator(
   task_id='send_email',
   to='tutor.dalmas.otieno@gmail.com',
   subject='Vaccine Updates in your area',
   html_content=""" <h3>Vaccine updates in your area</h3> """,
   files=['/tmp/vaccine.json'],
   dag=dag #Reference to the DAG variable
)

# Set the order of execution of tasks. 
download_vaccine_details >> notify_user >> email