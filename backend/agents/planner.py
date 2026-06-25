from llm import safe_generate
from langsmith import traceable

def _is_llm_failure(text: str) -> bool:
    if not text:
        return True
    lowered = text.lower()
    return any(x in lowered for x in [
        "llm generation unavailable",
        "quota exceeded",
        "generation failed",
        "rate limit",
        "permission-denied",
    ])

@traceable
def planner_node(state):
    print("Planning...")

    query = state["query"]

    prompt = f"""
You are an expert research planner.

Break the topic into 5 detailed research areas.

Topic:
{query}
"""

    plan = safe_generate(prompt)

    if _is_llm_failure(plan):
        plan = f"""
1. Market size and growth of {query}
2. Competitive landscape and key players in {query}
3. Technology architecture, AI models, and implementation stack for {query}
4. Future trends, automation opportunities, and industry adoption for {query}
5. Risks, limitations, and strategic recommendations for {query}
""".strip()

    state["plan"] = plan
    return state