import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from bs4 import BeautifulSoup

MODEL_NAME = "all-MiniLM-L6-v2"

# 1. Load and chunk SEC filing

import re
def load_and_chunk_html(file_path, chunk_size=500, overlap=100, keywords=None):
    html = Path(file_path).read_text()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Sentence-based chunking with overlap
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = ' '.join(sentences[i:i+chunk_size])
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
    file_path = "data/sec/apple_10k_2023.html"
    chunks = load_and_chunk_html(file_path)
    embeddings = embed_chunks(chunks)
    store_faiss(embeddings)
