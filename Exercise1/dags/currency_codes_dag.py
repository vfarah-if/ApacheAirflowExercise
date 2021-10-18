import json
from datetime import datetime, timedelta
import os
import logging

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

logger = logging.getLogger('airflow.task')
logger.info('Currency codes ...')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 10, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': 'vincent.farah@madetech.com'
}

currency_codes_data_path = f'{json.loads(BaseHook.get_connection("data_path").get_extra()).get("path")}/currency-codes.csv'
transformed_currency_codes_path = f'{os.path.splitext(currency_codes_data_path)[0]}-transformed.csv'

def transform_currency_codes_data(*args, **kwargs):
    currency_codes_data = pd.read_csv(filepath_or_buffer=currency_codes_data_path,
                                sep=',',
                                header=0,
                                usecols=['country','currency','code','number'],
                                index_col=0
                                )
    currency_codes_data.to_csv(path_or_buf=transformed_currency_codes_path)

def store_currency_codes_in_db(*args, **kwargs):
    transformed_currency_codes = pd.read_csv(transformed_currency_codes_path)
    transformed_currency_codes.dropna(axis=0, how='any', inplace=True)
    engine = make_engine()
    transformed_currency_codes.to_sql('currency_codes',engine,if_exists='replace',chunksize=500,index=False)

def make_engine()->Engine:
    connection_string = 'postgresql://airflow:airflow@postgres/exercise1'
    return create_engine(connection_string)
      
with DAG(dag_id='currency_codes_dag',
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    
    transform_currency_codes_data = PythonOperator(
        task_id='transform_currency_codes_data',
        python_callable=transform_currency_codes_data
    )

    create_table_currency_codes_if_not_exists = PostgresOperator(
        task_id='create_table_currency_codes_if_not_exists',
        sql='''CREATE TABLE IF NOT EXISTS currency_codes (
                id INT GENERATED ALWAYS AS IDENTITY,
                code VARCHAR(3) NOT NULL,
                country VARCHAR(100) NOT NULL,
                currency VARCHAR(50) NOT NULL,
                number INTEGER NOT NULL
                );''',
        postgres_conn_id='postgres',
        database='exercise1'
    )
    
    save_currency_codes_into_db = PythonOperator(
         task_id='save_currency_codes_into_db',
         python_callable=store_currency_codes_in_db
     )

    transform_currency_codes_data >> create_table_currency_codes_if_not_exists >> save_currency_codes_into_db
    