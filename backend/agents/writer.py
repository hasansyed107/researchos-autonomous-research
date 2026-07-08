import re



from llm import safe_generate
from langsmith import traceable

# =========================================================
# Configuration
# =========================================================

MAX_SECTION = 1200
MAX_REVIEW = 500
MAX_SOURCES = 3
MAX_SOURCE_SNIPPET = 100


# =========================================================
# Helpers
# =========================================================

def _safe_text(value) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, list):
        return "\n".join(
            str(v).strip() for v in value if v
        ).strip()

    return str(value).strip()


def _strip_heading(text: str) -> str:
    """
    Removes duplicated headings produced by upstream agents.
    """

    text = _safe_text(text)

    headings = [
        "Executive Summary",
        "Market Analysis",
        "Technology Analysis",
        "Future Trends",
        "Review Notes",
        "Fact Check",
    ]

    for heading in headings:

        pattern = rf"^{re.escape(heading)}\s*:?\s*"

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
        )

    return text.strip()


def _compress(text: str, limit: int = MAX_SECTION):
    """
    Compress text while preserving complete paragraphs.
    """

    text = _safe_text(text)

    if len(text) <= limit:
        return text

    paragraphs = re.split(r"\n\s*\n", text)

    output = []
    total = 0

    for para in paragraphs:

        para = para.strip()

        if not para:
            continue

        if total + len(para) > limit:
            break

        output.append(para)
        total += len(para)

    return "\n\n".join(output)


def _dedupe(text: str):
    """
    Remove duplicate lines while preserving markdown headings.
    """

    text = _safe_text(text)

    seen = set()
    output = []

    for line in text.splitlines():

        raw = line.rstrip()

        if raw.startswith("#"):
            output.append(raw)
            continue

        key = raw.strip()

        if not key:
            output.append("")
            continue

        if key in seen:
            continue

        seen.add(key)
        output.append(raw)

    return "\n".join(output).strip()


def _safe_results(source_obj):

    if not isinstance(source_obj, dict):
        return []

    results = source_obj.get("results", [])

    if not isinstance(results, list):
        return []

    cleaned = []
    seen = set()

    for item in results:

        if not isinstance(item, dict):
            continue

        title = _safe_text(item.get("title"))
        url = _safe_text(item.get("url"))

        key = (title, url)

        if key in seen:
            continue

        seen.add(key)

        cleaned.append(
            {
                "title": title or "Untitled",
                "content": _safe_text(
                    item.get("content")
                ),
            }
        )

        if len(cleaned) >= MAX_SOURCES:
            break

    return cleaned


def _is_llm_failure(text: str):

    if not text:
        return True

    text = text.lower().strip()

    failures = [
        "quota exceeded",
        "generation failed",
        "llm generation unavailable",
        "rate limit",
        "permission denied",
        "writer failed",
        "failed to generate",
        "internal error",
        "unavailable",
        "no report generated",
    ]

    return (
        any(f in text for f in failures)
        or len(text) < 120
    )


def _format_sources(results, section):

    if not results:
        return f"No {section.lower()} sources."

    output = []

    for i, item in enumerate(results, 1):

        snippet = " ".join(
            item["content"].split()
        )[:MAX_SOURCE_SNIPPET]

        output.append(
            f"""[{i}] {item['title']}

Evidence:
{snippet}
"""
        )

    return "\n\n".join(output)


def _format_chunks(chunks, title):

    if not chunks:
        return f"{title}\nNo PDF evidence."

    seen = set()
    output = []

    for chunk in chunks:

        chunk = str(chunk).strip()

        if not chunk:
            continue

        if chunk in seen:
            continue

        seen.add(chunk)

        output.append(f"- {chunk}")

        if len(output) >= 5:
            break

    return title + "\n" + "\n".join(output)


def _prepare(state):
    """
    Compress, clean and deduplicate all upstream outputs
    before sending them to the writer model.
    """

    return {

        "query":
            _safe_text(state.get("query")),

        "plan":
            _compress(
                state.get("plan"),
                700,
            ),

        "summary":
            _strip_heading(
                _compress(
                    state.get("research_summary"),
                    MAX_SECTION,
                )
            ),

        "market":
            _dedupe(
                _strip_heading(
                    _compress(
                        state.get("market_research"),
                        MAX_SECTION,
                    )
                )
            ),

        "technology":
            _dedupe(
                _strip_heading(
                    _compress(
                        state.get("technology_research"),
                        MAX_SECTION,
                    )
                )
            ),

        "trends":
            _dedupe(
                _strip_heading(
                    _compress(
                        state.get("trends_research"),
                        MAX_SECTION,
                    )
                )
            ),

        "review":
            _strip_heading(
                _compress(
                    state.get("review"),
                    MAX_REVIEW,
                )
            ),

        "fact":
            _strip_heading(
                _compress(
                    state.get("fact_check"),
                    MAX_REVIEW,
                )
            ),

        "market_sources":
            _safe_results(
                state.get("market_sources")
            ),

        "technology_sources":
            _safe_results(
                state.get("technology_sources")
            ),

        "trends_sources":
            _safe_results(
                state.get("trends_sources")
            ),

        "market_chunks":
            state.get("market_chunks", []) or [],

        "technology_chunks":
            state.get("technology_chunks", []) or [],

        "trends_chunks":
            state.get("trends_chunks", []) or [],
    }

# =========================================================
# Deterministic Fallback Report
# =========================================================

def _build_non_llm_report(state):
    """
    Build a deterministic report when the writer LLM fails.
    This guarantees a readable report even if generation fails.
    """

    data = _prepare(state)

    sections = []

    sections.append("# Research Report")

    sections.append(
f"""
## Topic

{data["query"]}
"""
    )

    sections.append(
f"""
## Executive Summary

{data["summary"] or "Not enough evidence available."}
"""
    )

    sections.append(
f"""
## Market Analysis

{data["market"] or "Not enough evidence available."}
"""
    )

    sections.append(
f"""
## Technology Analysis

{data["technology"] or "Not enough evidence available."}
"""
    )

    sections.append(
f"""
## Future Trends

{data["trends"] or "Not enough evidence available."}
"""
    )

    if data["review"]:
        sections.append(
f"""
## Review Notes

{data["review"]}
"""
        )

    if data["fact"]:
        sections.append(
f"""
## Fact Check

{data["fact"]}
"""
        )

    sections.append(
f"""
## Market Sources

{_format_sources(
    data["market_sources"],
    "Market"
)}
"""
    )

    sections.append(
f"""
## Technology Sources

{_format_sources(
    data["technology_sources"],
    "Technology"
)}
"""
    )

    sections.append(
f"""
## Trend Sources

{_format_sources(
    data["trends_sources"],
    "Trend"
)}
"""
    )

    sections.append(
f"""
## Retrieved PDF Evidence

{_format_chunks(
    data["market_chunks"],
    "### Market Chunks"
)}

{_format_chunks(
    data["technology_chunks"],
    "### Technology Chunks"
)}

{_format_chunks(
    data["trends_chunks"],
    "### Trend Chunks"
)}
"""
    )

    report = "\n\n".join(sections)

    # Cleanup

    report = re.sub(r"\n{3,}", "\n\n", report)
    report = report.strip()

    return report
# =========================================================
# Writer Node
# =========================================================

@traceable
def writer_node(state):

    print("Writing report...")

    data = _prepare(state)

    # -------------------------------------------------
    # Fallback if all upstream agents failed
    # -------------------------------------------------

    if (
        _is_llm_failure(data["summary"])
        and _is_llm_failure(data["market"])
        and _is_llm_failure(data["technology"])
        and _is_llm_failure(data["trends"])
    ):

        return {
            "title": data["query"] or "Research Report",
            "report": _build_non_llm_report(state),
        }

    # =====================================================
    # Optimized Writer Prompt (Lower Token Usage)
    # =====================================================

    prompt = f"""
You are a senior research consultant.

Generate a polished executive report.

IMPORTANT

- Use ONLY supplied evidence.
- Never invent facts.
- Never invent statistics.
- Never invent CAGR.
- Never invent companies.
- Never invent technologies.
- Never invent references.
- If evidence is missing write:
  "Not enough evidence available."

Return VALID GitHub Markdown.

Do NOT output HTML.

Do NOT output ASCII tables.

Every major section begins with ##

Every subsection begins with ###

Leave one blank line after every heading.

Use ONLY markdown tables.

Do NOT repeat information between sections.

Keep paragraphs under three sentences.

------------------------------------------------

## Executive Summary

Write 2 concise paragraphs covering

- Market
- Technology
- Opportunities
- Risks

------------------------------------------------

## Key Findings

Markdown table

| Area | Finding |
|------|---------|

6-8 findings.

------------------------------------------------

## Market Analysis

### Market Snapshot

| Metric | Value |
|--------|-------|
| Market Size | |
| Growth | |
| Leading Region | |
| Commercial Stage | |

Unknown values:
Not available.

### Market Drivers

Bullet list.

### Competitive Landscape

Not enough evidence available.

Only companies supported by evidence.

### Commercial Signals

Bullet list.

### Market Challenges

Bullet list.

### Key Takeaway

One bullet.

------------------------------------------------

## Technology Analysis

Technology ONLY.

No market discussion.

### Current Technology

Maximum two paragraphs.

### Technology Comparison

| Technology | Maturity | Advantages | Limitations |

### Current Capabilities

Bullets.

### Technical Challenges

Bullets.

### Infrastructure Requirements

Bullets.

### Key Takeaway

One bullet.

------------------------------------------------

## Future Trends

### Emerging Trends

Bullets.

### Adoption Outlook

| Timeframe | Expected Development |

### Key Takeaway

One bullet.

------------------------------------------------

## Strategic Recommendations

Use a numbered markdown list.

Example:

1. Recommendation
2. Recommendation
3. Recommendation
4. Recommendation

Do NOT restart numbering.

Each recommendation contains

Recommendation

Reason

Expected Impact

Supporting Evidence

------------------------------------------------

## Risks

| Risk | Impact | Supporting Evidence |

------------------------------------------------

## Conclusion

Maximum two short paragraphs.

------------------------------------------------

## Source Coverage

Bullet list only.

Mention

- Market Sources
- Technology Sources
- Trend Sources

Never reproduce URLs.

==================================================
EXECUTIVE SUMMARY
==================================================

{data["summary"]}

==================================================
MARKET
==================================================

{data["market"]}

==================================================
TECHNOLOGY
==================================================

{data["technology"]}

==================================================
TRENDS
==================================================

{data["trends"]}

==================================================
MARKET SOURCES
==================================================

{_format_sources(data["market_sources"], "Market")}

==================================================
TECHNOLOGY SOURCES
==================================================

{_format_sources(data["technology_sources"], "Technology")}

==================================================
TREND SOURCES
==================================================

{_format_sources(data["trends_sources"], "Trend")}
"""

    report = _safe_text(safe_generate(prompt))

    if _is_llm_failure(report):

        print("Writer failed. Using deterministic fallback.")

        report = _build_non_llm_report(state)

        report = re.sub(
        r"(## Executive Summary\s*\n*){2,}",
        "## Executive Summary\n\n",
        report,
        flags=re.MULTILINE,
        )

    report = report.replace("■", "-")
    report = report.replace("–", "-")
    report = report.replace("—", "-")
    report = report.strip()

    # -------------------------------------------------
    # Final fallback
    # -------------------------------------------------

    

    # -------------------------------------------------
    # Final cleanup
    # -------------------------------------------------

    

    return {
        "title": data["query"] or "Research Report",
        "report": report,
    }