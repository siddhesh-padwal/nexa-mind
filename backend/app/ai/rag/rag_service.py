from __future__ import annotations

from typing import Any


class MemoryService:
    def __init__(self) -> None:
        self.session_memory: dict[str, dict[str, Any]] = {}

    def store_context(self, conversation_id: str, key: str, value: Any) -> None:
        entry = self.session_memory.setdefault(conversation_id, {})
        entry[key] = value

    def get_context(self, conversation_id: str) -> dict[str, Any]:
        return self.session_memory.get(conversation_id, {})

    def summarize_history(self, history: list[dict[str, str]]) -> str:
        if not history:
            return "No recent context."

        recent = history[-6:]
        context_parts = []
        for item in recent:
            role = item.get("role", "user")
            content = item.get("content", "")
            if content:
                context_parts.append(f"{role}: {content}")
        return " | ".join(context_parts)
