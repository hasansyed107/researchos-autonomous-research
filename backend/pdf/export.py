from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from .styles import PAGE_MARGIN, HEADING1
from .components import cover_page, footer, summary_box
from .parser import parse_markdown


def _extract_summary(report: str):
    lines = report.split("\n")

    capture = False
    summary = []

    for line in lines:

        if line.startswith("## Executive Summary"):
            capture = True
            continue

        if capture and line.startswith("## "):
            break

        if capture:
            summary.append(line)

    return "\n".join(summary).strip()


def generate_pdf(topic: str, report: str):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        leftMargin=PAGE_MARGIN,
        rightMargin=PAGE_MARGIN,
        topMargin=PAGE_MARGIN,
        bottomMargin=PAGE_MARGIN,
    )

    story = []

    story.extend(cover_page(topic))

    story.append(
        Paragraph(
            "Research Report",
            HEADING1,
        )
    )

    story.append(Spacer(1, 10))

    # No custom Executive Summary
    story.extend(parse_markdown(report))

    doc.build(
        story,
        onFirstPage=footer,
        onLaterPages=footer,
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes