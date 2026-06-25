from llm import safe_generate
from langsmith import traceable


# =========================================================
# Helpers
# =========================================================

def _safe_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(v).strip() for v in value if v).strip()
    return str(value).strip()


def _safe_results(source_obj):
    if not isinstance(source_obj, dict):
        return []
    results = source_obj.get("results", [])
    if not isinstance(results, list):
        return []
    cleaned = []
    for item in results[:8]:
        if isinstance(item, dict):
            cleaned.append({
                "title": str(item.get("title", "Untitled")).strip(),
                "url": str(item.get("url", "")).strip(),
                "content": str(item.get("content", "")).strip(),
            })
    return cleaned


def _is_llm_failure(text: str) -> bool:
    if not text:
        return True

    lowered = text.lower().strip()
    failure_markers = [
        "llm generation unavailable",
        "quota exceeded",
        "generation failed",
        "rate limit",
        "permission-denied",
        "failed to generate",
        "no report generated",
        "error generating report",
        "writer failed",
        "unavailable",
    ]

    if any(x in lowered for x in failure_markers):
        return True

    if len(lowered) < 80:
        return True

    return False


def _format_sources(results, section_name: str) -> str:
    if not results:
        return f"No {section_name.lower()} sources available."

    lines = []
    for i, item in enumerate(results[:5], 1):
        title = item["title"] or "Untitled"
        url = item["url"] or "N/A"
        content = (item["content"] or "No content available.")[:300]

        lines.append(
            f"""### {i}. {title}
**Source:** {url}

{content}
"""
        )

    return "\n\n".join(lines)


def _format_chunks(chunks, title: str) -> str:
    chunks = chunks or []
    if not chunks:
        return f"### {title}\nNo PDF evidence available."

    bullet_list = "\n".join(f"- {str(c).strip()}" for c in chunks[:8] if str(c).strip())
    return f"### {title}\n{bullet_list}"


def _build_non_llm_report(state) -> str:
    """
    Deterministic fallback report builder.
    This is used when upstream LLM output is weak or when final generation fails.
    """
    query = _safe_text(state.get("query")) or "Research Topic"
    plan = _safe_text(state.get("plan"))
    summary = _safe_text(state.get("research_summary"))
    market = _safe_text(state.get("market_research"))
    technology = _safe_text(state.get("technology_research"))
    trends = _safe_text(state.get("trends_research"))
    review = _safe_text(state.get("review"))
    fact_check = _safe_text(state.get("fact_check"))

    market_sources = _safe_results(state.get("market_sources"))
    technology_sources = _safe_results(state.get("technology_sources"))
    trends_sources = _safe_results(state.get("trends_sources"))

    market_chunks = state.get("market_chunks", []) or []
    technology_chunks = state.get("technology_chunks", []) or []
    trends_chunks = state.get("trends_chunks", []) or []

    sections = [f"# Research Report\n\n## Topic\n{query}"]

    if plan:
        sections.append(f"## Research Plan\n{plan}")

    if summary:
        sections.append(f"## Executive Summary\n{summary}")

    if market:
        sections.append(f"## Market Analysis\n{market}")

    if technology:
        sections.append(f"## Technology Analysis\n{technology}")

    if trends:
        sections.append(f"## Future Trends\n{trends}")

    if review:
        sections.append(f"## Review Notes\n{review}")

    if fact_check:
        sections.append(f"## Fact Check\n{fact_check}")

    sections.append("## Source Evidence")
    sections.append(f"### Market Sources\n{_format_sources(market_sources, 'Market')}")
    sections.append(f"### Technology Sources\n{_format_sources(technology_sources, 'Technology')}")
    sections.append(f"### Trends Sources\n{_format_sources(trends_sources, 'Trends')}")

    sections.append("## Retrieved PDF Evidence")
    sections.append(_format_chunks(market_chunks, "Market Chunks"))
    sections.append(_format_chunks(technology_chunks, "Technology Chunks"))
    sections.append(_format_chunks(trends_chunks, "Trends Chunks"))

    return "\n\n---\n\n".join([s for s in sections if s and s.strip()])


# =========================================================
# Writer node
# =========================================================

@traceable
def writer_node(state):
    print("Writing...")

    query = _safe_text(state.get("query")) or "Research Report"

    plan = _safe_text(state.get("plan"))[:900]
    summary = _safe_text(state.get("research_summary"))[:1800]
    market = _safe_text(state.get("market_research"))[:1200]
    technology = _safe_text(state.get("technology_research"))[:1200]
    trends = _safe_text(state.get("trends_research"))[:1200]
    review = _safe_text(state.get("review"))[:700]
    fact_check = _safe_text(state.get("fact_check"))[:700]

    market_sources = _safe_results(state.get("market_sources"))
    technology_sources = _safe_results(state.get("technology_sources"))
    trends_sources = _safe_results(state.get("trends_sources"))

    # -----------------------------------------------------
    # Hard fallback if core research failed
    # -----------------------------------------------------
    if (
        _is_llm_failure(summary)
        and _is_llm_failure(market)
        and _is_llm_failure(technology)
        and _is_llm_failure(trends)
    ):
        report = _build_non_llm_report(state)
        return {
            "title": query,
            "report": report,
        }

    # -----------------------------------------------------
    # Grounded writer prompt
    # IMPORTANT:
    # - Only synthesize from supplied evidence
    # - Do not invent figures / citations
    # - If evidence is missing, explicitly say so
    # -----------------------------------------------------
    prompt = f"""
You are a senior research editor. Your job is to produce a final research report ONLY from the supplied material below.

STRICT RULES:
1. Use ONLY the evidence provided in:
   - Research Plan
   - Executive Summary
   - Market Analysis Draft
   - Technology Analysis Draft
   - Trends Analysis Draft
   - Review Notes
   - Fact Check Notes
   - Source snippets
2. DO NOT invent statistics, market sizes, CAGR values, company financials, dates, or references that do not appear in the provided material.
3. DO NOT create fake citation markers like [1], [2], etc. unless those exact citations already exist in the provided material.
4. If a section lacks evidence, say so explicitly instead of making it up.
5. Preserve nuance and uncertainty from the fact-check/review notes.
6. Output valid markdown only.

Write a concise, professional report with this structure:

# Executive Summary
# Key Findings
# Market Analysis
# Technology Analysis
# Future Trends
# Strategic Recommendations
# Risks and Challenges
# Conclusion
# Source Notes

Additional requirements:
- Maximum 1400 words
- Be analytical and practical
- Prefer plain language over hype
- Recommendations must be directly supported by the supplied material
- In "Source Notes", summarize the available source coverage rather than inventing academic references

========================
RESEARCH PLAN
========================
{plan or "No research plan provided."}

========================
EXECUTIVE SUMMARY DRAFT
========================
{summary or "No executive summary provided."}

========================
MARKET ANALYSIS DRAFT
========================
{market or "No market analysis provided."}

========================
TECHNOLOGY ANALYSIS DRAFT
========================
{technology or "No technology analysis provided."}

========================
TRENDS ANALYSIS DRAFT
========================
{trends or "No trends analysis provided."}

========================
REVIEW NOTES
========================
{review or "No review notes provided."}

========================
FACT CHECK NOTES
========================
{fact_check or "No fact check notes provided."}

========================
MARKET SOURCE SNIPPETS
========================
{_format_sources(market_sources, "Market")}

========================
TECHNOLOGY SOURCE SNIPPETS
========================
{_format_sources(technology_sources, "Technology")}

========================
TRENDS SOURCE SNIPPETS
========================
{_format_sources(trends_sources, "Trends")}
"""

    report = _safe_text(safe_generate(prompt))

    # -----------------------------------------------------
    # If final generation is weak, use deterministic report
    # -----------------------------------------------------
    if _is_llm_failure(report):
        report = _build_non_llm_report(state)

    return {
        "title": query,
        "report": report,
    }