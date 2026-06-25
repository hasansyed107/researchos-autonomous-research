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
def technology_researcher_node(state):
    print("Researching technology...")

    query = state["query"]
    chunks = state.get("technology_chunks", []) or []

    try:
        search_results = search_tavily(f"{query} technology architecture models benchmarks infrastructure")
    except Exception as e:
        print(f"Tavily error: {e}")
        search_results = {"results": []}

    state["technology_sources"] = search_results

    source_text = format_sources_for_prompt(search_results)
    chunk_text = format_chunks_for_prompt(chunks)

    prompt = f"""
You are a technology research analyst.

Your task is to write ONLY the technology analysis section for the topic below.

TOPIC:
{query}

STRICT RULES:
1. Use ONLY the evidence provided below.
2. Do NOT invent architectures, benchmarks, model performance, product capabilities, infrastructure details, or implementation claims.
3. If evidence is weak or conflicting, say so clearly.
4. Distinguish current capabilities from future claims.
5. Output valid markdown only.

Focus on:
- Architecture / system design
- Models / technical stack
- Benchmarks / performance evidence
- Infrastructure / deployment requirements
- Technical limitations / tradeoffs

Structure:
## Technology Analysis
### Core Technology Stack
### Performance / Benchmark Evidence
### Infrastructure and Deployment Considerations
### Technical Risks / Limitations

WEB SOURCES
{source_text}

DOCUMENT EVIDENCE
{chunk_text}
"""

    try:
        research = safe_generate(prompt)
    except Exception as e:
        print(f"Technology research LLM error: {e}")
        research = ""

    if is_llm_failure(research):
        research = build_research_fallback_section(
            title="Technology Analysis",
            query=query,
            search_results=search_results,
            chunks=chunks,
        )

    state["technology_research"] = research
    return state