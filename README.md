
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
- `mlflow_tracking/` - MLflow tracking utilities
- `app.py` - Streamlit app (main entry point)
- `data/sec/` - Downloaded and sample SEC filings

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Ingest and embed data: `python ingestion/sec_ingest.py` then `python rag/embed_and_store.py`
3. Run the UI: `streamlit run app.py`
4. Use the UI to search for litigation, risk, and compliance issues in filings

## Example Use Cases
- List potential litigation risks in a 10-K
- Compare debt covenants across quarters
- Summarize ESG compliance sections
- Detect unusual spikes in transaction logs

---
This project is for educational and demonstration purposes.
