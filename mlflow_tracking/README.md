# MLflow Tracking

This folder is intended for MLflow tracking artifacts, experiment logs, and pipeline orchestration scripts.

Currently, MLflow is used in `llm/llm_answer.py` to log LLM query parameters, latency, and outputs. However, no MLflow tracking server or pipeline orchestration is set up yet.

## Next Steps
- Add a Dockerfile to containerize the app and MLflow server
- Add an Airflow DAG to orchestrate the pipeline (ingestion, embedding, retrieval, LLM, tracking)
- Store MLflow artifacts in this folder or a mounted volume
