
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from rag.retrieve import FaissRetriever
from llm.llm_answer import answer_with_llm
from rag.embed_and_store import load_and_chunk_html

# Example: List potential litigation risks in Apple’s latest 10-K
if __name__ == "__main__":
    file_path = "data/sec/apple_10k_2023.html"
    faiss_path = "data/sec/faiss.index"
    keywords = ["litigation", "risk", "legal", "lawsuit", "proceeding", "regulatory", "compliance"]
    chunks = load_and_chunk_html(file_path, chunk_size=10, overlap=2, keywords=keywords)
    retriever = FaissRetriever(faiss_path, chunks, keywords=keywords)
    query = "List potential litigation risks in this 10-K."
    context = retriever.retrieve(query, top_k=5)
    answer = answer_with_llm(query, context)
    print("\n---\nLLM Answer:\n", answer)
