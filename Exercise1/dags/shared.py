from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

def make_engine()->Engine:
    connection_string = 'postgresql://airflow:airflow@postgres/exercise1'
    return create_engine(connection_string)
