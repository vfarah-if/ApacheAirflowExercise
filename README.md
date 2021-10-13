# Introduction
Analysis on **[Apache Airflow](https://airflow.apache.org/)** (AA) and collation of interesting documentation, videos and examples to help setup and run through docker, for help to develop using this very interesting tool. I just recently came across this tool and a practical application for its use with a government project I am consulting on, and found this to be a very facinating tool to add to my arsenal for solving software engineering problems. 

AA is an open source platform to programmatically orchestrate workflows. This has a built in chronological schedular and a very interesting workflow mechanism for creating task oriented solutions that can run several things sequentially and in parallel. Some slides have been shared for [Introducing Apache Airflow](./introducing-apache-airflow-slides.pdf).

Why should you learn AA? Extensibility, Reliability, Scalable and ale to guarantee SLA's.

## Exercise

- Docker compose up or down the docker implementation that can be found on the [docker setup](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

  ```makefile
  // Start it up
  make aaf-up
  make aaf-down
  ```

- Follow tutorial for more details withom the docker setup

- After running the docker compose up, you should have a logon on localhost to help facilitate any changes needed, default is airflow for both

  ![image-20211012162006419](./login-airflow.png)

- Once logged in there will be several example to look at or use as examples

  ![image-20211012162503619](./home-dags.png)

- **[Concepts](https://airflow.apache.org/docs/apache-airflow/1.10.12/concepts.html)**

  - In Airflow, a `DAG` – or a **Directed Acyclic Graph** – is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies

  - A DAG is defined in a ***Python script*** and needs to be in a dags folder

  - a DAG describes ***how*** you want to carry out your workflow

  - The happy flow consists of the following stages:

    1. **No status** (scheduler created empty task instance)
    2. **Scheduled** (scheduler determined task instance needs to run)
    3. **Queued** (scheduler sent task to executor to run on the queue)
    4. **Running** (worker picked up a task and is now running it)
    5. **Success** (task completed)

  - DAG parameters

    - **dag_id**: Who you atr

    - **start_date**: When it starts

    - **schedule_interval**: How often to run

    - **catchup**: Should this rerun because of a prior error if set to true

    - others parameters exist but those are the core params to run with 

      ```python
      from airflow import DAG
      from airflow.operators.bash import BashOperator
      
      with DAG(
          dag_id='example_bash_operator',
          schedule_interval='0 0 * * *',
          start_date=datetime(2021, 1, 1),
          catchup=False,
          dagrun_timeout=timedelta(minutes=60),
          tags=['example', 'example2'],
          params={"example_key": "example_value"},
      ) as dag:
          # Actual implementation to run to completion ...
      ```

  - Operators define mechanisms of action, like the PythonOperator

    ![image-20211013093831004](./operators.png)

  - Workflows are visually shown in the UI in the order they will execute on the web server using the scheduler

    ![image-20211013094031105](./workflow-sequence.png)

  - Once executed, a **Meta Database** stores all the workflow executions with a tasks' state and duration, users and roles and external connections

    `Schedular => Meta DB => Webserver => Execute workflows using the executor `

  - The executor 

- Alternatively follow the video found [here](https://www.youtube.com/watch?v=k-9GQa2eAsM) for links to doing it locally

## References

- https://app.pluralsight.com/library/courses/productionalizing-data-pipelines-apache-airflow/table-of-contents and working examples can be found at https://github.com/axel-sirota/productionalizing-data-pipelines-airflow

