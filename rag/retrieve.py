import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class FaissRetriever:
    def __init__(self, faiss_path, chunks, keywords=None):
        self.index = faiss.read_index(faiss_path)
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks = chunks
        self.keywords = keywords or [
            "litigation",
            "risk",
            "legal",
            "lawsuit",
            "proceeding",
            "regulatory",
            "compliance",
        ]

    def retrieve(self, query, top_k=5):
        # First, filter chunks by keywords for relevance
        filtered = [
            (i, c)
            for i, c in enumerate(self.chunks)
            if any(kw in c.lower() for kw in self.keywords)
        ]
        if filtered and len(filtered) >= top_k:
            idxs, filtered_chunks = zip(*filtered)
            q_emb = self.model.encode([query]).astype(np.float32)
            emb_filtered = self.model.encode(filtered_chunks).astype(np.float32)
            temp_index = faiss.IndexFlatL2(emb_filtered.shape[1])
            temp_index.add(emb_filtered)
            D, I = temp_index.search(q_emb, min(top_k, len(filtered_chunks)))
            return [filtered_chunks[i] for i in I[0] if i < len(filtered_chunks)]
        else:
            # Fallback to all chunks
            if not self.chunks:
                return []
            q_emb = self.model.encode([query]).astype(np.float32)
            D, I = self.index.search(q_emb, min(top_k, len(self.chunks)))
            return [self.chunks[i] for i in I[0] if i < len(self.chunks)]
