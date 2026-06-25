from llm import safe_generate
from langsmith import traceable
from agents.research_utils import (
    is_llm_failure,
    format_sources_for_prompt,
    format_chunks_for_prompt,
)


@traceable
def fact_checker_node(state):
    print("Fact Checking...")

    summary = state.get("research_summary", "")
    if is_llm_failure(summary):
        state["fact_check"] = """
## Verified Claims
- Source retrieval completed.
- Research workflow reached the fact-check stage.

## Unsupported Claims
- No reliable synthesized summary was available to validate.

## Contradictions
- None assessed automatically.

## Missing Evidence
- Summary-level claim validation could not be completed.

## High-Risk Issues
- Final report may rely on fallback synthesis or incomplete evidence.

## Confidence Assessment
Low
""".strip()
        return state

    market_sources = format_sources_for_prompt(state.get("market_sources", {}))
    technology_sources = format_sources_for_prompt(state.get("technology_sources", {}))
    trends_sources = format_sources_for_prompt(state.get("trends_sources", {}))

    market_chunks = format_chunks_for_prompt(state.get("market_chunks", [])[:5])
    technology_chunks = format_chunks_for_prompt(state.get("technology_chunks", [])[:5])
    trends_chunks = format_chunks_for_prompt(state.get("trends_chunks", [])[:5])

    prompt = f"""
You are a fact-checking analyst.

Validate the research summary against the available evidence.

STRICT RULES:
1. Only assess support using the supplied source snippets and document evidence.
2. Do not introduce new facts.
3. If a claim cannot be validated from the supplied evidence, mark it unsupported or weakly supported.
4. Be conservative.

RESEARCH SUMMARY
{summary[:5000]}

MARKET SOURCES
{market_sources}

TECHNOLOGY SOURCES
{technology_sources}

TRENDS SOURCES
{trends_sources}

MARKET DOCUMENT EVIDENCE
{market_chunks}

TECHNOLOGY DOCUMENT EVIDENCE
{technology_chunks}

TRENDS DOCUMENT EVIDENCE
{trends_chunks}

Output format:
## Verified Claims
## Unsupported Claims
## Contradictions
## Missing Evidence
## High-Risk Issues
## Confidence Assessment
"""

    try:
        fact_check = safe_generate(prompt)
    except Exception:
        fact_check = ""

    if is_llm_failure(fact_check):
        fact_check = """
## Verified Claims
- Source retrieval completed across market, technology, and trends stages.

## Unsupported Claims
- Could not fully validate synthesized claims in this run.

## Contradictions
- None automatically confirmed.

## Missing Evidence
- Claim-level validation against sources was incomplete.

## High-Risk Issues
- Quantitative claims should be manually reviewed before external use.

## Confidence Assessment
Medium-Low
""".strip()

    state["fact_check"] = fact_check
    return state