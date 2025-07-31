
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from rag.retrieve import FaissRetriever
from llm.llm_answer import answer_with_llm
from rag.embed_and_store import load_and_chunk_html

st.set_page_config(page_title="GenAI Risk & Compliance Analyst", layout="wide")
st.title("GenAI Risk & Compliance Analyst for SEC Filings")

# Let user select which 10-K to query
import glob

tenk_files = sorted(glob.glob("data/sec/*.htm"))
file_labels = [f.split("/")[-1] for f in tenk_files]
selected_idx = st.selectbox(
    "Select 10-K file to query:", range(len(file_labels)), format_func=lambda i: file_labels[i]
)
file_path = tenk_files[selected_idx]
faiss_path = "data/sec/faiss.index"
keywords = ["litigation", "risk", "legal", "lawsuit", "proceeding", "regulatory", "compliance"]
section_headers = ["risk factors", "legal proceedings", "litigation", "regulatory", "compliance"]

@st.cache_resource
def get_chunks(path):
    return load_and_chunk_html(
        path, chunk_size=10, overlap=2, keywords=keywords, section_headers=section_headers
    )

@st.cache_resource
def get_retriever(path):
    chunks = get_chunks(path)
    return FaissRetriever(faiss_path, chunks, keywords=keywords)

query = st.text_input("Enter your risk/compliance query:", "")

if st.button("Search") and query.strip():
    retriever = get_retriever(file_path)
    with st.spinner("Retrieving and generating answer..."):
        context = retriever.retrieve(query, top_k=5)
        answer = answer_with_llm(query, context)
        st.subheader("LLM Answer:")
        st.write(answer)
        st.subheader("Retrieved Context:")
        for i, chunk in enumerate(context):
            st.markdown(f"**Chunk {i+1}:**\n{chunk}")
