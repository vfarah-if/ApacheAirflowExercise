# Introduction
Analysis on **[Apache Airflow](https://airflow.apache.org/)** and collation of interesting documentation, videos and examples to help setup and run through docker, for help to develop using this very interesting tool. I just recently came across this tool and a practical application for its use with a government project I am consulting on, and found this to be a very facinating tool to add to my arsenal for solving software engineering problems. This has a built in chronological schedular and a very interesting workflow mechanism for creating task oriented solutions that can run several things sequentially and in parallel. Some slides have been shared for [Introducing Apache Airflow](./introducing-apache-airflow-slides.pdf).

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
  - A DAG is defined in a ***Python script***
  - a DAG describes ***how*** you want to carry out your workflow
  - The happy flow consists of the following stages:
    1. **No status** (scheduler created empty task instance)
    2. **Scheduled** (scheduler determined task instance needs to run)
    3. **Queued** (scheduler sent task to executor to run on the queue)
    4. **Running** (worker picked up a task and is now running it)
    5. **Success** (task completed)
  - 

- Alternatively follow the video found [here](https://www.youtube.com/watch?v=k-9GQa2eAsM) for links to doing it locally

## References

- https://app.pluralsight.com/library/courses/productionalizing-data-pipelines-apache-airflow/table-of-contents

