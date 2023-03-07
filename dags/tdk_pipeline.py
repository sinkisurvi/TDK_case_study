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
    'TDK_Use_Case_Pipeline',
    default_args=default_args,
    schedule_interval='40 23 * * *' # Run once a day at 23:40
)

log_save = BashOperator(
    task_id='log_save',
    bash_command="curl -X POST -H 'Content-Type: application/json' -d '{\"args\": [\"/opt/airflow/src/tdk_usecase.py\"]}' http://spark-worker:4000/commands/pyspark",
    dag=dag
)


log_save