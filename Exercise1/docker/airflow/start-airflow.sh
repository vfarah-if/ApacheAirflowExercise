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
# Create an API URL to be utilised with exchange api containing your API key and modify the path below or in the ADMIN folder
# Register on  https://manage.exchangeratesapi.io/dashboard
airflow variables --json --set 'exchange_url' 'http://api.exchangeratesapi.io/v1/latest?access_key=GET_YOURS'

exec airflow webserver  &> /dev/null &

exec airflow scheduler
