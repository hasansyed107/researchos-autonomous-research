from datetime import datetime
from typing import Any

from graph.workflow import workflow
from tools.pdf_loader import load_pdf
from tools.rag_pipeline import process_document
from mlops.mlflow_tracking import log_research_run


# =========================================================
# Helpers
# =========================================================

def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return "\n".join(str(v) for v in value if v is not None).strip()
    return str(value).strip()


def _safe_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value).strip()]


def _safe_sources(value: Any) -> dict:
    """
    Normalize Tavily / search source payloads into:
    {
        "results": [
            {"title": "...", "url": "...", "content": "..."}
        ]
    }
    """
    if not value:
        return {"results": []}

    if isinstance(value, dict):
        results = value.get("results", [])
        if isinstance(results, list):
            cleaned = []
            for item in results:
                if isinstance(item, dict):
                    cleaned.append({
                        "title": str(item.get("title", "Untitled")).strip(),
                        "url": str(item.get("url", "")).strip(),
                        "content": str(item.get("content", "")).strip(),
                    })
            return {"results": cleaned}

    return {"results": []}


def _looks_like_failed_report(text: str) -> bool:
    """
    More robust than just checking rate-limit messages.
    """
    if not text:
        return True

    lowered = text.lower().strip()

    failure_markers = [
        "quota exceeded",
        "generation failed",
        "llm generation unavailable",
        "rate limit",
        "permission-denied",
        "failed to generate",
        "no report generated",
        "error generating report",
        "writer failed",
        "unavailable",
    ]

    if any(marker in lowered for marker in failure_markers):
        return True

    # Extremely short "report" is probably junk
    if len(lowered) < 120:
        return True

    return False


def _format_rag_chunks(chunks: list[str], heading: str) -> str:
    if not chunks:
        return f"### {heading}\nNo relevant PDF insights found."

    lines = "\n".join(f"- {chunk}" for chunk in chunks[:8])
    return f"### {heading}\n{lines}"


def _format_search_results(source_obj: dict, section_title: str) -> str:
    results = source_obj.get("results", [])
    if not results:
        return f"No {section_title.lower()} sources available."

    formatted = []
    for i, item in enumerate(results[:5], 1):
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        content = item.get("content", "No summary available.")

        formatted.append(
            f"""### {i}. {title}
**Source:** {url or "N/A"}

{content}
"""
        )

    return "\n\n".join(formatted)


def _build_fallback_report(
    query: str,
    plan: str,
    market_research: str,
    technology_research: str,
    trends_research: str,
    research_summary: str,
    review: str,
    fact_check: str,
    market_sources: dict,
    technology_sources: dict,
    trends_sources: dict,
    rag_data: dict,
) -> str:
    """
    Canonical report builder when writer output is missing / low quality.
    """
    sections = [
        f"# Research Report\n\n## Topic\n{query}",
    ]

    if plan:
        sections.append(f"## Research Plan\n{plan}")

    if research_summary:
        sections.append(f"## Executive Summary\n{research_summary}")

    if market_research:
        sections.append(f"## Market Research\n{market_research}")

    if technology_research:
        sections.append(f"## Technology Research\n{technology_research}")

    if trends_research:
        sections.append(f"## Trends Research\n{trends_research}")

    if review:
        sections.append(f"## Review Notes\n{review}")

    if fact_check:
        sections.append(f"## Fact Check\n{fact_check}")

    sections.append("## Source Evidence")

    sections.append(
        f"""### Market Sources
{_format_search_results(market_sources, "Market Research")}"""
    )

    sections.append(
        f"""### Technology Sources
{_format_search_results(technology_sources, "Technology Research")}"""
    )

    sections.append(
        f"""### Trends Sources
{_format_search_results(trends_sources, "Trends Research")}"""
    )

    sections.append("## PDF / RAG Insights")
    sections.append(_format_rag_chunks(rag_data.get("market_chunks", []), "Market Chunks"))
    sections.append(_format_rag_chunks(rag_data.get("technology_chunks", []), "Technology Chunks"))
    sections.append(_format_rag_chunks(rag_data.get("trends_chunks", []), "Trends Chunks"))

    return "\n\n---\n\n".join([s for s in sections if s and s.strip()])


# =========================================================
# Main service
# =========================================================

async def run_research(query: str, file=None):
    query = (query or "").strip()
    if not query:
        return {
            "title": "",
            "query": "",
            "report": "",
            "generated_at": datetime.utcnow().isoformat(),
            "plan": "",
            "market_research": "",
            "technology_research": "",
            "trends_research": "",
            "research_summary": "",
            "review": "",
            "fact_check": "",
            "market_sources": {"results": []},
            "technology_sources": {"results": []},
            "trends_sources": {"results": []},
            "market_chunks": [],
            "technology_chunks": [],
            "trends_chunks": [],
            "llm_failed": True,
            "error": "Query is required.",
        }

    rag_data = {
        "market_chunks": [],
        "technology_chunks": [],
        "trends_chunks": [],
    }

    # -----------------------------------------------------
    # PDF processing
    # -----------------------------------------------------
    if file:
        try:
            pdf_text = load_pdf(file.file)
            rag_data = process_document(pdf_text, query) or rag_data
        except Exception as e:
            print(f"[PDF PROCESSING ERROR] {e}")

    # -----------------------------------------------------
    # Run graph
    # -----------------------------------------------------
    try:
        result = workflow.invoke({
            "query": query,
            "market_chunks": rag_data.get("market_chunks", []),
            "technology_chunks": rag_data.get("technology_chunks", []),
            "trends_chunks": rag_data.get("trends_chunks", []),
        }) or {}
    except Exception as e:
        print(f"[WORKFLOW ERROR] {e}")
        result = {}

    print("\n===== WORKFLOW RESULT =====")
    print(result)
    print("===========================\n")

    # -----------------------------------------------------
    # Normalize graph outputs
    # -----------------------------------------------------
    title = _safe_str(result.get("title")) or query
    plan = _safe_str(result.get("plan"))
    market_research = _safe_str(result.get("market_research"))
    technology_research = _safe_str(result.get("technology_research"))
    trends_research = _safe_str(result.get("trends_research"))
    research_summary = _safe_str(result.get("research_summary"))
    review = _safe_str(result.get("review"))
    fact_check = _safe_str(result.get("fact_check"))
    raw_report = _safe_str(result.get("report"))

    market_sources = _safe_sources(result.get("market_sources"))
    technology_sources = _safe_sources(result.get("technology_sources"))
    trends_sources = _safe_sources(result.get("trends_sources"))

    rag_data = {
        "market_chunks": _safe_list(rag_data.get("market_chunks")),
        "technology_chunks": _safe_list(rag_data.get("technology_chunks")),
        "trends_chunks": _safe_list(rag_data.get("trends_chunks")),
    }

    # -----------------------------------------------------
    # Decide whether writer output is good enough
    # -----------------------------------------------------
    llm_failed = _looks_like_failed_report(raw_report)

    if llm_failed:
        report = _build_fallback_report(
            query=query,
            plan=plan,
            market_research=market_research,
            technology_research=technology_research,
            trends_research=trends_research,
            research_summary=research_summary,
            review=review,
            fact_check=fact_check,
            market_sources=market_sources,
            technology_sources=technology_sources,
            trends_sources=trends_sources,
            rag_data=rag_data,
        )
    else:
        report = raw_report

    # -----------------------------------------------------
    # Tracking
    # -----------------------------------------------------
    try:
        log_research_run(query=query, report_length=len(report))
    except Exception as e:
        print(f"[MLFLOW ERROR] {e}")

    # -----------------------------------------------------
    # Stable API response
    # -----------------------------------------------------
    return {
        "title": title,
        "query": query,
        "report": report,
        "generated_at": datetime.utcnow().isoformat(),

        "plan": plan,
        "market_research": market_research,
        "technology_research": technology_research,
        "trends_research": trends_research,
        "research_summary": research_summary,
        "review": review,
        "fact_check": fact_check,

        "market_sources": market_sources,
        "technology_sources": technology_sources,
        "trends_sources": trends_sources,

        "market_chunks": rag_data["market_chunks"],
        "technology_chunks": rag_data["technology_chunks"],
        "trends_chunks": rag_data["trends_chunks"],

        "llm_failed": llm_failed,
        "error": "",
    }