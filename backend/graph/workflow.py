from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import ResearchState

from agents.planner import planner_node

from agents.market_researcher import (
    market_researcher_node
)

from agents.technology_researcher import (
    technology_researcher_node
)

from agents.trends_researcher import (
    trends_researcher_node
)

from agents.summarizer import (
    summarizer_node
)

from agents.reviewer import (
    reviewer_node
)

from agents.fact_checker import (
    fact_checker_node
)

from agents.writer import (
    writer_node
)


graph = StateGraph(
    ResearchState
)


# ====================================
# Nodes
# ====================================

graph.add_node(
    "planner",
    planner_node
)

graph.add_node(
    "market_researcher",
    market_researcher_node
)

graph.add_node(
    "technology_researcher",
    technology_researcher_node
)

graph.add_node(
    "trends_researcher",
    trends_researcher_node
)

graph.add_node(
    "summarizer",
    summarizer_node
)

graph.add_node(
    "reviewer",
    reviewer_node
)

graph.add_node(
    "fact_checker",
    fact_checker_node
)

graph.add_node(
    "writer",
    writer_node
)


# ====================================
# Flow
# ====================================

graph.add_edge(
    START,
    "planner"
)

graph.add_edge(
    "planner",
    "market_researcher"
)

graph.add_edge(
    "market_researcher",
    "technology_researcher"
)

graph.add_edge(
    "technology_researcher",
    "trends_researcher"
)

graph.add_edge(
    "trends_researcher",
    "summarizer"
)

graph.add_edge(
    "summarizer",
    "reviewer"
)

graph.add_edge(
    "reviewer",
    "fact_checker"
)

graph.add_edge(
    "fact_checker",
    "writer"
)

graph.add_edge(
    "writer",
    END
)

workflow = graph.compile()