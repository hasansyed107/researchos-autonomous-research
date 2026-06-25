from llm import safe_generate
from langsmith import traceable
from agents.research_utils import (
    is_llm_failure,
    format_sources_for_prompt,
    format_chunks_for_prompt,
)


@traceable
def reviewer_node(state):
    print("Reviewing...")

    summary = state.get("research_summary", "")
    if is_llm_failure(summary):
        state["review"] = """
## Strengths
- Source retrieval completed across research stages.
- Workflow executed end-to-end.

## Weaknesses
- Research synthesis quality is limited because summary generation failed.

## Missing Areas
- No reliable cross-section synthesis was produced.

## Improvement Recommendations
- Retry with a working LLM or use deterministic section assembly.

## Strategic Opportunities
- Preserve source-first evidence blocks and expose them directly in the UI.
""".strip()
        return state

    market = state.get("market_research", "")[:3000]
    technology = state.get("technology_research", "")[:3000]
    trends = state.get("trends_research", "")[:3000]

    market_sources = format_sources_for_prompt(state.get("market_sources", {}))
    technology_sources = format_sources_for_prompt(state.get("technology_sources", {}))
    trends_sources = format_sources_for_prompt(state.get("trends_sources", {}))

    market_chunks = format_chunks_for_prompt(state.get("market_chunks", [])[:5])
    technology_chunks = format_chunks_for_prompt(state.get("technology_chunks", [])[:5])
    trends_chunks = format_chunks_for_prompt(state.get("trends_chunks", [])[:5])

    prompt = f"""
You are a senior research reviewer.

Review the research summary against the underlying evidence and identify quality issues.

STRICT RULES:
- Do not add new facts.
- Only evaluate support, completeness, clarity, and strategic usefulness.

RESEARCH SUMMARY
{summary[:5000]}

MARKET SECTION
{market}

TECHNOLOGY SECTION
{technology}

TRENDS SECTION
{trends}

MARKET SOURCES
{market_sources}

TECHNOLOGY SOURCES
{technology_sources}

TRENDS SOURCES
{trends_sources}

MARKET RAG EVIDENCE
{market_chunks}

TECHNOLOGY RAG EVIDENCE
{technology_chunks}

TRENDS RAG EVIDENCE
{trends_chunks}

Output format:
## Strengths
## Weaknesses
## Missing Areas
## Unsupported or Overstated Claims
## Improvement Recommendations
## Strategic Opportunities

Maximum 500 words.
"""

    try:
        review = safe_generate(prompt)
    except Exception:
        review = ""

    if is_llm_failure(review):
        review = """
## Strengths
- The workflow produced market, technology, and trends sections.
- Web sources and document evidence were collected.

## Weaknesses
- The review stage could not reliably validate the synthesis.

## Missing Areas
- Explicit source-to-claim validation remains incomplete.

## Unsupported or Overstated Claims
- Could not be assessed automatically in this run.

## Improvement Recommendations
- Surface source snippets alongside each section in the frontend.
- Add claim extraction + citation mapping in a later iteration.

## Strategic Opportunities
- Use this evidence-first structure to support auditable research reports.
""".strip()

    state["review"] = review
    return state