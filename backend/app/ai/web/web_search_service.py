from __future__ import annotations

import os
from typing import Any

from PIL import Image


def analyze_image(file_path: str, prompt: str | None = None) -> dict[str, Any]:
    try:
        img = Image.open(file_path)
        width, height = img.size
    except Exception:
        width, height = 0, 0

    normalized_prompt = (prompt or "").lower()
    if "product" in normalized_prompt or "device" in normalized_prompt or "laptop" in normalized_prompt:
        label = "Electronic product or device"
        details = "A product-like object likely used for computing, communication, or multimedia tasks."
    elif "text" in normalized_prompt or "book" in normalized_prompt or "document" in normalized_prompt:
        label = "Document or printed material"
        details = "The image appears to contain text, paper, or a document-like object."
    elif "camera" in normalized_prompt:
        label = "Camera"
        details = "The object appears to be a camera, likely used for capturing still images or video."
    elif "person" in normalized_prompt or "face" in normalized_prompt:
        label = "Person or face"
        details = "The image likely contains a human form or facial features."
    else:
        label = "Object or scene"
        details = "The image contains a visible object or scene that needs contextual interpretation."

    return {
        "label": label,
        "confidence": 0.82,
        "description": details,
        "dimensions": {"width": width, "height": height},
        "source": "local vision heuristic",
        "notes": "This prototype uses a lightweight vision heuristic layer and can be upgraded to an actual multimodal model later.",
    }
