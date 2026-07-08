from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from reportlab.graphics.shapes import Drawing, Line

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from .styles import (
    TITLE_STYLE,
    SUBTITLE_STYLE,
    HEADING1,
    BODY,
    SMALL,
    PRIMARY,
    PRIMARY_DARK,
    BORDER,
    TABLE_ALT,
    TABLE_ROW,
)


# -------------------------------------------------------
# Horizontal Divider
# -------------------------------------------------------

def divider():
    d = Drawing(450, 12)

    d.add(
        Line(
            0,
            6,
            450,
            6,
            strokeColor=BORDER,
            strokeWidth=1,
        )
    )

    return d


# -------------------------------------------------------
# Cover Page
# -------------------------------------------------------

def cover_page(topic: str):

    story = []

    story.append(Spacer(1, 1.0 * inch))

    story.append(
        Paragraph(
            "ResearchOS",
            TITLE_STYLE,
        )
    )

    story.append(
        Paragraph(
            "Autonomous Research Intelligence",
            SUBTITLE_STYLE,
        )
    )

    story.append(divider())

    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph(
            "<b>Research Topic</b>",
            HEADING1,
        )
    )

    story.append(
        Paragraph(
            topic,
            BODY,
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    story.append(
        Paragraph(
            "<b>Generated</b>",
            HEADING1,
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime("%d %B %Y %H:%M"),
            BODY,
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    story.append(
        Paragraph(
            "<b>Workflow</b>",
            HEADING1,
        )
    )

    story.append(
        Paragraph(
            "Planner → Market → Technology → Trends → Reviewer → Fact Checker → Writer",
            BODY,
        )
    )

    story.append(Spacer(1, 1.2 * inch))

    story.append(divider())

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "Prepared by ResearchOS",
            SMALL,
        )
    )

    story.append(PageBreak())

    return story


# -------------------------------------------------------
# Executive Summary Box
# -------------------------------------------------------

def summary_box(text):

    table = Table(
        [[Paragraph(text, BODY)]],
        colWidths=[6.5 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF8FC")),
                ("BOX", (0, 0), (-1, -1), 1, PRIMARY),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    return table


# -------------------------------------------------------
# Nice Section Title
# -------------------------------------------------------

def section(title):

    return [
        Spacer(1, 18),
        divider(),
        Spacer(1, 8),
        Paragraph(title, HEADING1),
        Spacer(1, 4),
    ]


# -------------------------------------------------------
# Styled Table
# -------------------------------------------------------

def findings_table(rows):

    data = [["Finding", "Evidence"]]

    data.extend(rows)

    table = Table(
        data,
        colWidths=[3.2 * inch, 3.3 * inch],
    )

    style = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]

    for i in range(1, len(data)):
        bg = TABLE_ALT if i % 2 == 0 else TABLE_ROW
        style.append(("BACKGROUND", (0, i), (-1, i), bg))

    table.setStyle(TableStyle(style))

    return table


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

def footer(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    canvas.setFillColor(colors.grey)

    canvas.drawString(
        doc.leftMargin,
        20,
        "ResearchOS • Autonomous Research Intelligence",
    )

    canvas.drawRightString(
        doc.width + doc.leftMargin,
        20,
        f"Page {doc.page}",
    )

    canvas.restoreState()