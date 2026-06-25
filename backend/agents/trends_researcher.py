from tools.search import search_tavily
from llm import safe_generate
from langsmith import traceable

from agents.research_utils import (
    is_llm_failure,
    format_sources_for_prompt,
    build_research_fallback_section,
    format_chunks_for_prompt,
)


@traceable
def trends_researcher_node(state):
    print("Researching trends...")

    query = state["query"]
    chunks = state.get("trends_chunks", []) or []

    try:
        search_results = search_tavily(f"{query} future trends predictions adoption outlook emerging technology")
    except Exception as e:
        print(f"Tavily error: {e}")
        search_results = {"results": []}

    state["trends_sources"] = search_results

    source_text = format_sources_for_prompt(search_results)
    chunk_text = format_chunks_for_prompt(chunks)

    prompt = f"""
You are a research analyst focused on future trends.

Your task is to write ONLY the future trends section for the topic below.

TOPIC:
{query}

STRICT RULES:
1. Use ONLY the evidence provided below.
2. Do NOT invent forecasts, adoption timelines, market predictions, or future technology claims.
3. Clearly separate:
   - already observable trends
   - forward-looking predictions from sources
   - your own inference based on evidence
4. If there is weak evidence for long-term predictions, say so.
5. Output valid markdown only.

Focus on:
- Emerging trends
- Future adoption patterns
- workflow / automation changes
- industry shifts
- plausible medium-term outlook based on evidence

Structure:
## Future Trends
### Observable Trends Today
### Emerging Signals
### Forward-Looking Outlook
### Uncertainties / Watchpoints

WEB SOURCES
{source_text}

DOCUMENT EVIDENCE
{chunk_text}
"""

    try:
        research = safe_generate(prompt)
    except Exception as e:
        print(f"Trends research LLM error: {e}")
        research = ""

    if is_llm_failure(research):
        research = build_research_fallback_section(
            title="Future Trends",
            query=query,
            search_results=search_results,
            chunks=chunks,
        )

    state["trends_research"] = research
    return state