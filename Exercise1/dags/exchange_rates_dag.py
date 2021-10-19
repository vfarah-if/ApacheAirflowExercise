from datetime import datetime, timedelta
import os
import requests
import logging

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from shared import make_engine

logger = logging.getLogger('airflow.task')
logger.info('Exchange Rates information...')

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
ex_rates_data_path = f'{Variable.get("data_path")}/exchange-rates.csv'
transformed_ex_rates_path = f'{os.path.splitext(ex_rates_data_path)[0]}-transformed.csv'

def transform_ex_rates_data(*args, **kwargs):
    ex_rates_data = pd.read_csv(filepath_or_buffer=ex_rates_data_path,
                                      sep=',',
                                      header=0,
                                      usecols=['code','rate','base_rate_code','date'],
                                      parse_dates=['date'],
                                      index_col=0
                                     )
    ex_rates_data.to_csv(path_or_buf=transformed_ex_rates_path)

def load_csv_ex_rates_in_db(*args, **kwargs):   
    transformed_ex_rates = pd.read_csv(transformed_ex_rates_path)
    transformed_ex_rates.dropna(axis=0, how='any', inplace=True)
    engine = make_engine()
    transformed_ex_rates.to_sql('ex_rates',engine,if_exists='replace',chunksize=500,index=False)

def get_ex_rates_from_api():
    url = Variable.get('exchange_url')
    logger.info(f'Loading data from {url}')
    response = requests.get(url)
    logger.info(response)
    json_response = response.json()        
    logger.info(json_response)
    return json_response

def store_latest_ex_rates_from_api_to_db():
    rates_data = get_ex_rates_from_api()
    date = rates_data['date']
    logger.info('Date', date)
    base_rate_code = rates_data['base']
    logger.info('Base Code', base_rate_code)
    rates = rates_data['rates']
    logger.info(rates)
    engine = make_engine()    
    delete_rates_by_date(date, engine)
    if rates:
        for code, rate in rates.items():            
            add_exchange_rate(date, base_rate_code, engine, code, rate)

def add_exchange_rate(date, base_rate_code, engine, code, rate):
    logger.info(f'{code}, {rate}, {base_rate_code}, {date}')                       
    # TODO: Refactor using the ORM    
    insert_response = engine.execute(
                f'''
                    INSERT INTO ex_rates(code,rate,base_rate_code,date) 
                    VALUES ('{code}',{rate},'{base_rate_code}','{date}');
                '''
            )
    logger.info(f'Created "{insert_response.rowcount}" records')

def delete_rates_by_date(date, engine):
    if date:
        # TODO: Refactor using the ORM
        delete_response = engine.execute(f"DELETE FROM ex_rates WHERE date = '{date}'")
        logger.info(f'Deleted "{delete_response}" records')
       
with DAG(dag_id='exchange_rates_dag',
         schedule_interval='@daily',
         default_args=default_args,
         template_searchpath=[f"{os.environ['AIRFLOW_HOME']}"],
         catchup=False) as dag:
    
    # TODO: Refactor using ORM
    create_table_ex_rates_if_not_exists = PostgresOperator(
        task_id='create_table_ex_rates_if_not_exists',
        sql='''CREATE TABLE IF NOT EXISTS ex_rates (
                code VARCHAR(3) NOT NULL,
                rate DECIMAL NOT NULL,
                base_code VARCHAR(3) NOT NULL,
                date DATE NOT NULL,
                PRIMARY KEY (code, base_code, date)
                );''',
        postgres_conn_id='postgres',
        database='exercise1'
    )

    transform_ex_rates_data = PythonOperator(
        task_id='transform_ex_rates_data',
        python_callable=transform_ex_rates_data
    )

    save_csv_ex_rates_in_db = PythonOperator(
        task_id='save_csv_ex_rates_in_db',
        python_callable=load_csv_ex_rates_in_db
    )

    save_latest_ex_rates_from_api_to_db = PythonOperator(
        task_id='save_latest_ex_rates_from_api_to_db',
        python_callable=store_latest_ex_rates_from_api_to_db
    )

    transform_ex_rates_data >> create_table_ex_rates_if_not_exists >> save_csv_ex_rates_in_db
    create_table_ex_rates_if_not_exists >> save_latest_ex_rates_from_api_to_db
