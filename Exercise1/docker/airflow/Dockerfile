# Base Image
FROM puckel/docker-airflow

ENV AIRFLOW_HOME=/usr/local/airflow
WORKDIR $AIRFLOW_HOME
COPY ./start-airflow.sh $AIRFLOW_HOME/start-airflow.sh
COPY ./airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY ./currency-codes.csv $AIRFLOW_HOME/data/currency-codes.csv
COPY ./exchange-rates.csv $AIRFLOW_HOME/data/exchange-rates.csv
USER root
RUN chmod +x $AIRFLOW_HOME/start-airflow.sh
RUN chown -R airflow:airflow $AIRFLOW_HOME
USER airflow
CMD [ "./start-airflow.sh" ]
