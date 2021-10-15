CREATE ROLE postgres LOGIN SUPERUSER PASSWORD 'postgres';
CREATE DATABASE exchange_rates;
GRANT ALL PRIVILEGES ON DATABASE exchange_rates to airflow;
