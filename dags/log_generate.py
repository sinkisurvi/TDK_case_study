from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'TDK_Data_Arrival_simulation',
    default_args=default_args,
    schedule_interval='30 23 * * *' # Run once a day at 23:30
)

log_arrival = BashOperator(
    task_id='log_arrival',
    bash_command="python /opt/airflow/data/generate_log.py",
    dag=dag
)

log_arrival