# Airflow Orchestration

This folder contains Airflow DAGs for orchestrating the GenAI Risk & Compliance Analyst pipeline.

- `dag_genai_risk.py`: Example DAG to run ingestion, embedding, LLM, and start/stop services.

## Usage

To use Airflow with Docker, add the following to your docker-compose or run Airflow in a separate container with this folder mounted.

For local development:

```sh
pip install apache-airflow
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow webserver -p 8080 &
airflow scheduler &
```

Then add the DAG in the Airflow UI.
