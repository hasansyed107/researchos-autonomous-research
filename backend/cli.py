from services.research_service import (
    run_research
)

print("STARTING RESEARCHOS")

query = input(
    "Enter research topic: "
)

result = run_research(
    query
)

with open(
    "report.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        result["report"]
    )

print(
    "Report saved to report.md"
)