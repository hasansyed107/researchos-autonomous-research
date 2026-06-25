# test_stream.py

from graph.workflow import workflow

for event in workflow.stream(
    {
        "query": "AI Coding Assistants",
        "market_chunks": [],
        "technology_chunks": [],
        "trends_chunks": []
    }
):
    print(event)