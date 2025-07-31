
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from rag.retrieve import FaissRetriever
from llm.llm_answer import answer_with_llm
from rag.embed_and_store import load_and_chunk_html

# Example: List potential litigation risks in Apple’s latest 10-K
if __name__ == "__main__":
    file_path = "data/sec/sample_10k_apple_2022.htm"  # Use the known-good sample 10-K with litigation risk
    faiss_path = "data/sec/faiss.index"
    keywords = ["litigation", "risk", "legal", "lawsuit", "proceeding", "regulatory", "compliance"]
    section_headers = ["risk factors", "legal proceedings", "litigation", "regulatory", "compliance"]
    chunks = load_and_chunk_html(file_path, chunk_size=10, overlap=2, keywords=keywords, section_headers=section_headers)
    retriever = FaissRetriever(faiss_path, chunks, keywords=keywords)
    query = (
        "Extract and summarize all litigation risks mentioned in the following SEC 10-K filing. "
        "For each risk, provide a concise bullet point and reference the section or language if possible. "
        "Focus only on legal, regulatory, or litigation-related risks."
    )
    context = retriever.retrieve(query, top_k=5)
    answer = answer_with_llm(query, context)
    print("\n---\nLLM Answer:\n", answer)
