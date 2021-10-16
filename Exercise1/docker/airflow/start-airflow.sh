#!/usr/bin/env bash

# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow initdb
# shellcheck disable=SC2016
# Create a folder for CSV data
airflow connections --add --conn_id 'data_path' --conn_type File --conn_extra '{ "path" : "data" }'
# Create a postgress SQL connection to be utilised by a dag
airflow connections --add --conn_id 'postgres' --conn_type Postgres --conn_host 'postgres' --conn_login 'airflow' --conn_password 'airflow' --conn_schema 'exercise1'
exec airflow webserver  &> /dev/null &

exec airflow scheduler
