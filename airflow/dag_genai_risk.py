from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def ingest_sec_filings():
    from ingestion.sec_ingest import download_latest_10k
    download_latest_10k()

def embed_and_store():
    from rag.embed_and_store import embed_and_store_all
    embed_and_store_all()

def run_llm_query():
    from llm.llm_answer import answer_with_llm
    # Example query and context
    answer_with_llm("What are the main risks?", ["Example context chunk."])

def start_mlflow_server():
    os.system("mlflow server --backend-store-uri sqlite:///mlflow_tracking/mlflow.db --default-artifact-root ./mlflow_tracking --host 0.0.0.0 --port 5000 &")

def start_streamlit():
    os.system("streamlit run api/app.py &")

def stop_services():
    os.system("pkill -f mlflow")
    os.system("pkill -f streamlit")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'genai_risk_pipeline',
    default_args=default_args,
    description='GenAI Risk & Compliance Analyst Pipeline',
    schedule_interval=None,
    catchup=False,
)

t1 = PythonOperator(
    task_id='ingest_sec_filings',
    python_callable=ingest_sec_filings,
    dag=dag,
)
t2 = PythonOperator(
    task_id='embed_and_store',
    python_callable=embed_and_store,
    dag=dag,
)
t3 = PythonOperator(
    task_id='run_llm_query',
    python_callable=run_llm_query,
    dag=dag,
)
t4 = PythonOperator(
    task_id='start_mlflow_server',
    python_callable=start_mlflow_server,
    dag=dag,
)
t5 = PythonOperator(
    task_id='start_streamlit',
    python_callable=start_streamlit,
    dag=dag,
)
t6 = PythonOperator(
    task_id='stop_services',
    python_callable=stop_services,
    dag=dag,
)

t1 >> t2 >> t3
[t4, t5] >> t6
