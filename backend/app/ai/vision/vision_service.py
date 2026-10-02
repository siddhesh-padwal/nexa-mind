from __future__ import annotations

import hashlib
from typing import List

import numpy as np

try:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except Exception:
    model = None


def generate_embedding(text: str) -> List[float]:
    if model is not None:
        vector = model.encode([text])[0]
        return vector.astype(float).tolist()

    digest = hashlib.sha256(text.encode("utf-8")).digest()
    arr = np.frombuffer(digest, dtype=np.uint8).astype(float)
    if arr.size < 384:
        arr = np.pad(arr, (0, 384 - arr.size), constant_values=0.0)
    return arr[:384].tolist()
