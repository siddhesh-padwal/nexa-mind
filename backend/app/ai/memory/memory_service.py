from __future__ import annotations

import json
from typing import Any

import requests


def search_web(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": "1",
        "skip_disambig": "1",
    }

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        return []

    payload = response.json()
    results = []

    for item in payload.get("RelatedTopics", [])[:max_results]:
        if isinstance(item, dict):
            results.append(
                {
                    "title": item.get("Text", "Related result").split(" - ")[0][:120],
                    "url": item.get("FirstURL") or "",
                    "snippet": item.get("Text", "")[:300],
                }
            )

    if not results and payload.get("AbstractText"):
        results.append(
            {
                "title": payload.get("Heading") or "DuckDuckGo summary",
                "url": payload.get("AbstractURL") or "",
                "snippet": payload.get("AbstractText", "")[:400],
            }
        )

    return results
