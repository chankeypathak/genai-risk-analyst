
# GenAI Risk & Compliance Analyst for Financial Filings

## Overview
This project is a GenAI-powered assistant that analyzes SEC 10-K filings and other financial documents to extract key risks, litigation, and compliance issues. It uses Retrieval-Augmented Generation (RAG), tracks LLM prompts/responses with MLflow, and provides an interactive Streamlit UI for analysts.

## Key Features
- Ingests real SEC filings and sample filings
- RAG with FAISS for document retrieval
- LLM (Hugging Face) for risk extraction and summarization
- MLflow for prompt/response tracking
- Streamlit interface for interactive Q&A
- Prompt templates for risk/compliance

## Architecture
```mermaid
graph TD
    A[SEC Filings/Docs] -->|Ingestion| B[Chunking & Embedding]
    B -->|Vectors| C[FAISS Vector Store]
    C -->|Retrieval| D[Relevant Chunks]
    D -->|Prompt| E[LLM (Hugging Face)]
    E -->|Answer| F[Streamlit UI]
    E -->|Tracking| G[MLflow]
```

## Project Structure
- `ingestion/` - Data ingestion scripts
- `rag/` - RAG and vector store logic
- `llm/` - LLM and prompt templates
- `mlflow_tracking/` - MLflow tracking server, logs, and setup scripts
- `airflow/` - Airflow DAGs for pipeline orchestration
- `api/app.py` - Streamlit app (main entry point)
- `data/sec/` - Downloaded and sample SEC filings

## Getting Started
### Option 1: Run End-to-End Pipeline with Airflow
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize Airflow:
   ```sh
   export AIRFLOW_HOME=$(pwd)/airflow
   airflow db init
   airflow webserver -p 8080 &
   airflow scheduler &
   ```
3. In the Airflow UI (http://localhost:8080), enable and trigger the `genai_risk_pipeline` DAG for end-to-end orchestration (ingestion, embedding, LLM, MLflow, Streamlit).

### Option 2: Manual Steps (No Airflow)
1. Install dependencies: `pip install -r requirements.txt`
2. Start MLflow tracking server:
   ```sh
   bash mlflow_tracking/mlflow_setup.sh
   # or manually:
   mlflow server --backend-store-uri sqlite:///mlflow_tracking/mlflow.db --default-artifact-root ./mlflow_tracking --host 0.0.0.0 --port 5000
   ```
3. Ingest SEC filings: `python ingestion/sec_ingest.py`
4. Embed and store: `python rag/embed_and_store.py`
5. Run the Streamlit UI:
   ```sh
   streamlit run api/app.py
   ```
6. Use the UI to search for litigation, risk, and compliance issues in filings

### Option 3: Docker (Recommended for Production)
#### A. Single Container (Streamlit + MLflow)
1. Build the image:
   ```sh
   docker build -t genai-risk-analyst .
   ```
2. Run the container:
   ```sh
   docker run -p 8501:8501 -p 5000:5000 genai-risk-analyst
   ```
3. Access Streamlit at http://localhost:8501 and MLflow at http://localhost:5000

#### B. Full Orchestration with Docker Compose (Streamlit + MLflow + Airflow)
1. Start all services:
   ```sh
   docker-compose up --build
   ```
2. Access the UIs:
   - Streamlit: http://localhost:8501
   - MLflow: http://localhost:5000
   - Airflow: http://localhost:8080
3. In Airflow, enable and trigger the `genai_risk_pipeline` DAG for end-to-end orchestration.

## Example Use Cases
- List potential litigation risks in a 10-K
- Compare debt covenants across quarters
- Summarize ESG compliance sections
- Detect unusual spikes in transaction logs

---
