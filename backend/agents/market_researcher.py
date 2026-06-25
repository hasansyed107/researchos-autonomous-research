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
def market_researcher_node(state):
    print("Researching market...")

    query = state["query"]
    chunks = state.get("market_chunks", []) or []

    try:
        search_results = search_tavily(f"{query} market size competitors pricing adoption")
    except Exception as e:
        print(f"Tavily error: {e}")
        search_results = {"results": []}

    state["market_sources"] = search_results

    source_text = format_sources_for_prompt(search_results)
    chunk_text = format_chunks_for_prompt(chunks)

    prompt = f"""
You are a market research analyst.

Your task is to write ONLY the market/business analysis section for the topic below.

TOPIC:
{query}

STRICT RULES:
1. Use ONLY the evidence provided in the web sources and retrieved document evidence below.
2. Do NOT invent market size, CAGR, funding, pricing, adoption, revenue, or competitor facts.
3. If evidence is missing for a subtopic, explicitly say so.
4. Separate confirmed observations from inference.
5. Output valid markdown only.

Focus on:
- Market size / demand signals
- Growth drivers
- Competitors / market structure
- Pricing / monetization if available
- Adoption patterns
- Risks / uncertainty in the market evidence

Structure:
## Market Analysis
### Market Overview
### Competitive Landscape
### Commercial Signals
### Risks / Gaps in Evidence

WEB SOURCES
{source_text}

DOCUMENT EVIDENCE
{chunk_text}
"""

    try:
        research = safe_generate(prompt)
    except Exception as e:
        print(f"Market research LLM error: {e}")
        research = ""

    if is_llm_failure(research):
        research = build_research_fallback_section(
            title="Market Analysis",
            query=query,
            search_results=search_results,
            chunks=chunks,
        )

    state["market_research"] = research
    return state