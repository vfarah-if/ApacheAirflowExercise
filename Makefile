aaf-up:
	echo "Loading Apache Airflow to play with ..."
	docker compose up

aaf-down:
	echo "Stopping Apache Airflow to shutdown ..."
	docker compose down

aaf-db:
	airflow db init

test:
	pytest tests --cov=dataflow --cov-report=term-missing --ignore=./env