import json
from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 10, 14),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": "vincent.farah@madetech.com"
}

currency_codes_data_path = f'{json.loads(BaseHook.get_connection("data_path").get_extra()).get("path")}/currency-codes.csv'
transformed_currency_codes_path = f'{os.path.splitext(currency_codes_data_path)[0]}-transformed.csv'

ex_rates_data_path = f'{json.loads(BaseHook.get_connection("data_path").get_extra()).get("path")}/exchange-rates.csv'
transformed_ex_rates_path = f'{os.path.splitext(ex_rates_data_path)[0]}-transformed.csv'

def transform_currency_codes_data(*args, **kwargs):
    currency_codes_data = pd.read_csv(filepath_or_buffer=currency_codes_data_path,
                                sep=',',
                                header=0,
                                usecols=['country','currency','code','number'],
                                index_col=0
                                )
    currency_codes_data.to_csv(path_or_buf=transformed_currency_codes_path)

def transform_ex_rates_data(*args, **kwargs):
    ex_rates_data = pd.read_csv(filepath_or_buffer=ex_rates_data_path,
                                      sep=',',
                                      header=0,
                                      usecols=['code','rate','base_rate_code','date'],
                                      parse_dates=['date'],
                                      index_col=0
                                     )
    ex_rates_data.to_csv(path_or_buf=transformed_ex_rates_path)

def store_currency_codes_in_db(*args, **kwargs):
    transformed_currency_codes = pd.read_csv(transformed_currency_codes_path)
    # transformed_currency_codes.columns = [c.lower() for c in
    #                                 transformed_currency_codes.columns] 
    transformed_currency_codes.dropna(axis=0, how='any', inplace=True)
    engine = make_engine()
    transformed_currency_codes.to_sql('currency_codes',engine,if_exists='replace',chunksize=500,index=False)

def store_ex_rates_in_db(*args, **kwargs):   
    transformed_ex_rates = pd.read_csv(transformed_ex_rates_path)
    # transformed_ex_rates.columns = [c.lower() for c in
    #                                 transformed_ex_rates.columns] 
    transformed_ex_rates.dropna(axis=0, how='any', inplace=True)
    engine = make_engine()
    transformed_ex_rates.to_sql('ex_rates',engine,if_exists='replace',chunksize=500,index=False)

def make_engine()->Engine:
    connection_string = 'postgresql://airflow:airflow@postgres/exercise1'
    return create_engine(connection_string)
        
with DAG(dag_id="exchange_rates_dag",
         schedule_interval="@daily",
         default_args=default_args,
         template_searchpath=[f"{os.environ['AIRFLOW_HOME']}"],
         catchup=False) as dag:
    
    create_table_currency_codes = PostgresOperator(
        task_id='create_table_currency_codes',
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

    create_table_ex_rates = PostgresOperator(
        task_id='create_table_ex_rates',
        sql='''CREATE TABLE IF NOT EXISTS ex_rates (
                code VARCHAR(3) NOT NULL,
                rate DECIMAL NOT NULL,
                base_code VARCHAR(3) NOT NULL,
                date DATE NOT NULL
                );''',
        postgres_conn_id='postgres',
        database='exercise1'
    )

    transform_currency_codes_data = PythonOperator(
        task_id="transform_currency_codes_data",
        python_callable=transform_currency_codes_data
    )

    save_currency_codes_into_db = PythonOperator(
        task_id='save_currency_codes_into_db',
        python_callable=store_currency_codes_in_db
    )

    transform_ex_rates_data = PythonOperator(
        task_id="transform_ex_rates_data",
        python_callable=transform_ex_rates_data
    )

    save_ex_rates_into_db = PythonOperator(
        task_id='save_ex_rates_into_db',
        python_callable=store_ex_rates_in_db
    )

    transform_currency_codes_data >> create_table_currency_codes >> save_currency_codes_into_db
    transform_ex_rates_data >> create_table_ex_rates >> save_ex_rates_into_db
