import re

from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Table,
    TableStyle,
)

from .styles import (
    HEADING1,
    HEADING2,
    HEADING3,
    BODY,
    CODE,
    QUOTE,
)


# ---------------------------------------------------------
# Inline markdown formatting
# ---------------------------------------------------------

def _format_inline(text: str) -> str:

    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\u2011": "-",      # non-breaking hyphen
        "\u2013": "-",      # en dash
        "\u2014": "-",      # em dash
        "\u2212": "-",      # minus
        "\u2022": "•",
        "\u202F": " ",      # narrow no-break space
        "\u00A0": " ",      # nbsp
        "\u25A0": "",
        "■": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Bold
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text,
    )

    # Italic
    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text,
    )

    # Inline code
    text = re.sub(
        r"`(.*?)`",
        r"<font face='Courier'>\1</font>",
        text,
    )

    return text


# ---------------------------------------------------------
# Markdown table
# ---------------------------------------------------------

def _build_table(table_lines):

    rows = []

    for line in table_lines:

        cols = [
            Paragraph(
                _format_inline(col.strip()),
                BODY,
            )
            for col in line.strip().strip("|").split("|")
        ]

        rows.append(cols)

    table = Table(
        rows,
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    return table


# ---------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------

def parse_markdown(report: str):

    story = []

    lines = report.split("\n")

    in_code = False
    code_lines = []

    i = 0

    while i < len(lines):

        line = lines[i].rstrip()

        # -------------------------------------------------
        # Code block
        # -------------------------------------------------

        if line.startswith("```"):

            if not in_code:

                in_code = True
                code_lines = []

            else:

                in_code = False

                story.append(
                    Paragraph(
                        "<br/>".join(code_lines),
                        CODE,
                    )
                )

                story.append(Spacer(1, 12))

            i += 1
            continue

        if in_code:

            code_lines.append(
                line.replace("<", "&lt;").replace(">", "&gt;")
            )

            i += 1
            continue

        # -------------------------------------------------
        # Horizontal Rule
        # -------------------------------------------------

        if line.strip() in ("---", "***"):

            story.append(Spacer(1, 18))

            i += 1
            continue

        # -------------------------------------------------
        # Empty
        # -------------------------------------------------

        if not line.strip():

            story.append(Spacer(1, 6))

            i += 1
            continue

        # -------------------------------------------------
        # Markdown Table
        # -------------------------------------------------

        if line.startswith("|"):

            table_lines = []

            while i < len(lines) and lines[i].startswith("|"):

                table_lines.append(lines[i])

                i += 1

            if len(table_lines) > 1:

                separator = table_lines[1]

                if re.fullmatch(r"\|?[\-\s:|]+\|?", separator):

                    table_lines.pop(1)

            story.append(_build_table(table_lines))
            story.append(Spacer(1, 14))

            continue

        # -------------------------------------------------
        # H1
        # -------------------------------------------------

        if line.startswith("# "):

            story.append(
                Paragraph(
                    _format_inline(line[2:]),
                    HEADING1,
                )
            )

            story.append(Spacer(1, 8))

            i += 1
            continue

        # -------------------------------------------------
        # H2
        # -------------------------------------------------

        if line.startswith("## "):

            story.append(
                Paragraph(
                    _format_inline(line[3:]),
                    HEADING2,
                )
            )

            story.append(Spacer(1, 6))

            i += 1
            continue

        # -------------------------------------------------
        # H3
        # -------------------------------------------------

        if line.startswith("### "):

            story.append(
                Paragraph(
                    _format_inline(line[4:]),
                    HEADING3,
                )
            )

            story.append(Spacer(1, 6))

            i += 1
            continue

        # -------------------------------------------------
        # Quote
        # -------------------------------------------------

        if line.startswith(">"):

            story.append(
                Paragraph(
                    _format_inline(line[1:].strip()),
                    QUOTE,
                )
            )

            story.append(Spacer(1, 10))

            i += 1
            continue

        # -------------------------------------------------
        # Bullet List
        # -------------------------------------------------

        if line.startswith("- ") or line.startswith("* "):

            items = []

            while (
                i < len(lines)
                and (
                    lines[i].startswith("- ")
                    or lines[i].startswith("* ")
                )
            ):

                items.append(
                    ListItem(
                        Paragraph(
                            _format_inline(lines[i][2:].strip()),
                            BODY,
                        )
                    )
                )

                i += 1

            story.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                )
            )

            story.append(Spacer(1, 10))

            continue

        # -------------------------------------------------
        # Numbered List
        # -------------------------------------------------

        if re.match(r"^\d+\.", line):

            items = []

            while (
                i < len(lines)
                and re.match(r"^\d+\.", lines[i])
            ):

                text = re.sub(
                    r"^\d+\.\s*",
                    "",
                    lines[i],
                )

                items.append(
                    ListItem(
                        Paragraph(
                            _format_inline(text),
                            BODY,
                        )
                    )
                )

                i += 1

            story.append(
                ListFlowable(
                    items,
                    bulletType="1",
                    start="1",
                )
            )

            story.append(Spacer(1, 10))

            continue

        # -------------------------------------------------
        # Normal paragraph
        # -------------------------------------------------

        story.append(
            Paragraph(
                _format_inline(line),
                BODY,
            )
        )

        story.append(Spacer(1, 6))

        i += 1

    return story