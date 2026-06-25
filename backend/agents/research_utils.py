from typing import List, Dict, Any


def is_llm_failure(text: str) -> bool:
    if not text:
        return True

    lowered = text.lower().strip()
    markers = [
        "llm generation unavailable",
        "quota exceeded",
        "generation failed",
        "rate limit",
        "permission-denied",
        "failed to generate",
        "error",
    ]
    return any(m in lowered for m in markers)


def normalize_search_results(search_results: Dict[str, Any], max_items: int = 5) -> List[Dict[str, str]]:
    if not isinstance(search_results, dict):
        return []

    results = search_results.get("results", [])
    if not isinstance(results, list):
        return []

    normalized = []
    for item in results[:max_items]:
        if not isinstance(item, dict):
            continue

        normalized.append({
            "title": str(item.get("title", "Untitled")).strip(),
            "url": str(item.get("url", "")).strip(),
            "content": str(item.get("content", "")).strip(),
        })

    return normalized


def format_sources_for_prompt(search_results: Dict[str, Any], max_items: int = 5) -> str:
    results = normalize_search_results(search_results, max_items=max_items)

    if not results:
        return "No web sources available."

    blocks = []
    for i, item in enumerate(results, 1):
        blocks.append(
            f"""Source {i}
Title: {item["title"]}
URL: {item["url"]}
Snippet: {item["content"]}"""
        )

    return "\n\n".join(blocks)


def format_sources_for_report(search_results: Dict[str, Any], section_name: str, max_items: int = 5) -> str:
    results = normalize_search_results(search_results, max_items=max_items)

    if not results:
        return f"No {section_name.lower()} web sources available."

    lines = []
    for i, item in enumerate(results, 1):
        title = item["title"] or "Untitled"
        url = item["url"] or "N/A"
        content = item["content"] or "No content available."

        lines.append(
            f"""### {i}. {title}
**Source:** {url}

{content}
"""
        )

    return "\n\n".join(lines)


def format_chunks_for_prompt(chunks: List[str], max_items: int = 8) -> str:
    if not chunks:
        return "No document evidence available."

    cleaned = [str(c).strip() for c in chunks[:max_items] if str(c).strip()]
    if not cleaned:
        return "No document evidence available."

    return "\n\n".join(f"- {c}" for c in cleaned)


def build_research_fallback_section(
    title: str,
    query: str,
    search_results: Dict[str, Any],
    chunks: List[str],
) -> str:
    source_text = format_sources_for_report(search_results, title)
    chunk_text = format_chunks_for_prompt(chunks)

    return f"""
## {title}

### Topic Focus
{query}

### Web Evidence
{source_text}

### Retrieved Document Evidence
{chunk_text}

### Analyst Note
LLM synthesis was unavailable, so this section contains collected evidence rather than a synthesized narrative.
""".strip()