from typing import TypedDict, Optional


class ResearchState(TypedDict):

    # User Input
    query: str

    # Planning
    plan: Optional[str]

    # RAG Context
    market_chunks: Optional[list]
    technology_chunks: Optional[list]
    trends_chunks: Optional[list]

    # Research Outputs
    market_research: Optional[str]
    technology_research: Optional[str]
    trends_research: Optional[str]

    # Summarized Research
    research_summary: Optional[str]

    # Sources
    market_sources: Optional[str]
    technology_sources: Optional[str]
    trends_sources: Optional[str]

    # Review Stage
    review: Optional[str]

    # Fact Check Stage
    fact_check: Optional[str]

    # Final Report
    report: Optional[str]

    # Optional UI Title
    title: Optional[str]