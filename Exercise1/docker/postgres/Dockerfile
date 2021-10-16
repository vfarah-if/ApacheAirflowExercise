FROM library/postgres:12
COPY currency-codes.csv /
RUN chown postgres:postgres currency-codes.csv
COPY exchange-rates.csv /
RUN chown postgres:postgres exchange-rates.csv
COPY init.sql /docker-entrypoint-initdb.d/
