from __future__ import annotations

from typing import Any

from app.ai.memory.memory_service import MemoryService
from app.ai.rag.rag_service import RAGService
from app.ai.vision.vision_service import analyze_image
from app.ai.web.web_search_service import search_web


class AIOrchestrator:
    def __init__(self, rag_service: RAGService, memory_service: MemoryService) -> None:
        self.rag_service = rag_service
        self.memory_service = memory_service

    def handle_message(self, user_message: str, image_path: str | None = None, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
        history = history or []
        message_lower = user_message.lower()

        if image_path:
            visual_context = analyze_image(image_path, user_message)
        else:
            visual_context = None

        if "document" in message_lower or "uploaded" in message_lower or "search my" in message_lower:
            r_result = self.rag_service.search(user_message, top_k=3)
            return {
                "type": "document",
                "visual_context": visual_context,
                "retrieved": r_result,
                "answer": self._compose_grounded_answer(user_message, r_result, visual_context),
            }

        if "compare" in message_lower or "latest" in message_lower or "recent" in message_lower or "news" in message_lower or "search" in message_lower:
            web_results = search_web(user_message, max_results=3)
            return {
                "type": "web",
                "visual_context": visual_context,
                "retrieved": web_results,
                "answer": self._compose_web_answer(user_message, web_results, visual_context),
            }

        memory_context = self.memory_service.summarize_history(history)
        base_answer = "Based on the available context, this appears to be a relevant object or scene."

        if visual_context:
            base_answer = (
                f"I identified the image as: {visual_context['label']}. {visual_context['description']} "
                f"Confidence is {visual_context['confidence']:.2f}."
            )

        return {
            "type": "vision",
            "visual_context": visual_context,
            "retrieved": [],
            "answer": f"{base_answer} Conversation context: {memory_context}",
        }

    def _compose_grounded_answer(self, user_message: str, retrieved: list[dict[str, Any]], visual_context: dict[str, Any] | None) -> str:
        if not retrieved:
            return "I did not find relevant documents for this query. Please upload a document or rephrase the question."

        snippets = "\n".join(f"- {item['chunk'][:220]}" for item in retrieved[:3])
        if visual_context:
            return (
                f"I found relevant document content for '{user_message}'.\n"
                f"Visual context: {visual_context['label']}\n"
                f"Relevant excerpts:\n{snippets}"
            )
        return f"I found relevant document content for '{user_message}':\n{snippets}"

    def _compose_web_answer(self, user_message: str, results: list[dict[str, Any]], visual_context: dict[str, Any] | None) -> str:
        if not results:
            return "I could not retrieve reliable public data for this query."

        snippets = "\n".join(f"- {item['title']}: {item['snippet'][:200]}" for item in results[:3])
        if visual_context:
            return (
                f"I found web sources related to '{user_message}' and compared them with the image context.\n"
                f"Visual context: {visual_context['label']}\n"
                f"Sources:\n{snippets}"
            )
        return f"I found public sources for '{user_message}':\n{snippets}"
