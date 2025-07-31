# GenAI Risk & Compliance Analyst for Financial Filings

## Overview
This project is a GenAI-powered assistant that analyzes regulatory filings (10-K, 10-Q, etc.), contracts, investment portfolios, and audit logs to extract key risks, anomalies, and regulatory issues. It uses Retrieval-Augmented Generation (RAG), tracks LLM prompts/responses with MLflow, and provides an API/UI for analysts.

## Key Features
- Ingests real SEC filings, contracts, portfolios, and logs
- RAG with FAISS/Weaviate for document retrieval
- LLM (Hugging Face/OpenAI) for risk extraction and summarization
- MLflow for prompt/response tracking
- FastAPI/Streamlit interface
- Prompt templates for risk/compliance
- (Bonus) Airflow DAG for re-indexing, feedback loop

## Project Structure
- `ingestion/` - Data ingestion scripts
- `rag/` - RAG and vector store logic
- `llm/` - LLM and prompt templates
- `mlflow_tracking/` - MLflow tracking utilities
- `api/` - FastAPI/Streamlit app

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the API/UI: `python api/app.py` or `streamlit run api/app.py`
3. Ingest data and try example queries

## Example Use Cases
- List potential litigation risks in a 10-K
- Compare debt covenants across quarters
- Summarize ESG compliance sections
- Detect unusual spikes in transaction logs

---
This project is for educational and demonstration purposes.
