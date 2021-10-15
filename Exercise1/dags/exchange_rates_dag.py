from datetime import datetime, timedelta

from airflow import DAG

default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 10, 15),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


with DAG(dag_id="exchange_rates_dag",
         schedule_interval="@daily",
         default_args=default_args,
         catchup=False) as dag:
    None
