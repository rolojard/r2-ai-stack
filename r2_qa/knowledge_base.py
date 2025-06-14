#!/usr/bin/env python3
"""
KnowledgeBase:
  Ingests text passages, builds/loads a FAISS index of embeddings,
  and retrieves the top-k relevant passages for a query.
"""

import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

# Paths
DATA_DIR       = Path(__file__).parent / "demo_data"
INDEX_PATH     = DATA_DIR / "sw_index.faiss"
PASSAGES_PATH  = DATA_DIR / "sample_passages.json"
EMBED_MODEL    = "all-MiniLM-L6-v2"

class KnowledgeBase:
    def __init__(self):
        self.model    = SentenceTransformer(EMBED_MODEL)
        self.passages = json.loads(PASSAGES_PATH.read_text())
        if INDEX_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))
        else:
            self._build_index()

    def _build_index(self):
        texts = [p["text"] for p in self.passages]
        embs  = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        d     = embs.shape[1]
        self.index = faiss.IndexFlatIP(d)
        self.index.add(embs)
        faiss.write_index(self.index, str(INDEX_PATH))

    def retrieve(self, query: str, top_k: int = 3):
        q_emb = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        D, I  = self.index.search(q_emb, top_k)
        return [self.passages[i] for i in I[0]]
