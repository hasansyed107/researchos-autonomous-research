from llm import safe_generate
from langsmith import traceable
from agents.research_utils import is_llm_failure


def _trim(text, n=700):
    if not text:
        return ""
    return str(text).strip()[:n]


@traceable
def summarizer_node(state):
    print("Summarizing...")

    market = _trim(state.get("market_research", ""), 1000)
    technology = _trim(state.get("technology_research", ""), 1000)
    trends = _trim(state.get("trends_research", ""), 1000)

    prompt = f"""
You are a research synthesis editor.

Create a concise cross-section summary using ONLY the supplied section drafts.

STRICT RULES:
1. Use ONLY the supplied market, technology, and trends sections.
2. Do NOT introduce new facts, numbers, companies, timelines, or claims.
3. If one section is weak or evidence-light, mention that limitation.
4. Highlight cross-cutting patterns and tensions.
5. Output valid markdown only.
6. Keep the total output under 600 words.

Structure:
## Market Summary
## Technology Summary
## Trends Summary
## Cross-Cutting Takeaways

MARKET SECTION
{market}

TECHNOLOGY SECTION
{technology}

TRENDS SECTION
{trends}
"""

    try:
        summary = safe_generate(prompt)
    except Exception:
        summary = ""

    if is_llm_failure(summary):
        summary = f"""
## Market Summary
{_trim(state.get("market_research", "No market research available."), 700)}

## Technology Summary
{_trim(state.get("technology_research", "No technology research available."), 700)}

## Trends Summary
{_trim(state.get("trends_research", "No trends research available."), 700)}

## Cross-Cutting Takeaways
Summary generation failed, so a shortened version of the research sections is shown instead.
""".strip()

    state["research_summary"] = summary
    return state