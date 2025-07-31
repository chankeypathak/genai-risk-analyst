import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from bs4 import BeautifulSoup

MODEL_NAME = "all-MiniLM-L6-v2"

# 1. Load and chunk SEC filing

import re


def load_and_chunk_html(
    file_path, chunk_size=500, overlap=100, keywords=None, section_headers=None
):
    html = Path(file_path).read_text()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Section-aware chunking: extract sections with relevant headers
    section_headers = section_headers or [
        "risk factors",
        "legal proceedings",
        "litigation",
        "regulatory",
        "compliance",
    ]
    # Find section starts
    lower_text = text.lower()
    section_indices = []
    for header in section_headers:
        idx = lower_text.find(header)
        if idx != -1:
            section_indices.append((idx, header))
    section_indices.sort()
    # Extract sections
    chunks = []
    for i, (start_idx, header) in enumerate(section_indices):
        end_idx = section_indices[i + 1][0] if i + 1 < len(section_indices) else len(text)
        section = text[start_idx:end_idx].strip()
        if section:
            chunks.append(section)
    # Fallback: if no sections found, use previous sentence-based chunking
    if not chunks:
        import re

        sentences = re.split(r"(?<=[.!?]) +", text)
        i = 0
        while i < len(sentences):
            chunk = " ".join(sentences[i : i + chunk_size])
            if keywords:
                if any(kw in chunk.lower() for kw in keywords):
                    chunks.append(chunk)
            else:
                chunks.append(chunk)
            i += max(chunk_size - overlap, 1)
    return chunks


# 2. Embed chunks


def embed_chunks(chunks):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=True)
    return np.array(embeddings, dtype=np.float32)


# 3. Store in FAISS


def store_faiss(embeddings, faiss_path="data/sec/faiss.index"):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, faiss_path)
    print(f"Stored {embeddings.shape[0]} vectors in {faiss_path}")


if __name__ == "__main__":
    file_path = "data/sec/sample_10k_apple_2022.htm"
    chunks = load_and_chunk_html(file_path)
    embeddings = embed_chunks(chunks)
    store_faiss(embeddings)
