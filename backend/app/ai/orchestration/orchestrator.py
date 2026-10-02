from __future__ import annotations

import math
from typing import Any

from app.ai.embeddings.embedding_service import generate_embedding


class RAGService:
    def __init__(self) -> None:
        self.documents: list[dict[str, Any]] = []

    def add_document(self, filename: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        chunks = self._chunk_text(content)
        for idx, chunk in enumerate(chunks):
            self.documents.append(
                {
                    "filename": filename,
                    "chunk": chunk,
                    "metadata": metadata or {},
                    "index": idx,
                    "embedding": generate_embedding(chunk),
                }
            )

    def _chunk_text(self, text: str, chunk_size: int = 400) -> list[str]:
        text = text.strip()
        if not text:
            return []
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        if not self.documents:
            return []

        query_embedding = generate_embedding(query)
        scored = []

        for item in self.documents:
            similarity = self._cosine_similarity(query_embedding, item["embedding"])
            scored.append({"score": similarity, **item})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
