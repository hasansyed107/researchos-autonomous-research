from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont


# --------------------------------------------------
# Fonts
# --------------------------------------------------

try:
    registerFont(TTFont("Inter", "Inter-Regular.ttf"))
    registerFont(TTFont("Inter-Bold", "Inter-Bold.ttf"))

    BODY_FONT = "Inter"
    BOLD_FONT = "Inter-Bold"

except Exception:

    BODY_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"


# --------------------------------------------------
# Color Theme
# --------------------------------------------------

PRIMARY = colors.HexColor("#0F62FE")
PRIMARY_DARK = colors.HexColor("#0F172A")

TEXT = colors.HexColor("#1E293B")
LIGHT_TEXT = colors.HexColor("#64748B")

BACKGROUND = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#CBD5E1")

SUCCESS = colors.HexColor("#10B981")


# --------------------------------------------------
# Base stylesheet
# --------------------------------------------------

styles = getSampleStyleSheet()


# --------------------------------------------------
# Title
# --------------------------------------------------

TITLE_STYLE = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontName=BOLD_FONT,
    fontSize=28,
    leading=34,
    alignment=TA_CENTER,
    textColor=PRIMARY_DARK,
    spaceAfter=24,
)


SUBTITLE_STYLE = ParagraphStyle(
    "Subtitle",
    parent=styles["BodyText"],
    fontName=BODY_FONT,
    fontSize=12,
    leading=18,
    alignment=TA_CENTER,
    textColor=LIGHT_TEXT,
    spaceAfter=32,
)


# --------------------------------------------------
# Headings
# --------------------------------------------------

HEADING1 = ParagraphStyle(
    "Heading1",
    parent=styles["Heading1"],
    fontName=BOLD_FONT,
    fontSize=21,
    leading=28,
    textColor=PRIMARY_DARK,
    spaceBefore=22,
    spaceAfter=12,
)


HEADING2 = ParagraphStyle(
    "Heading2",
    parent=styles["Heading2"],
    fontName=BOLD_FONT,
    fontSize=17,
    leading=24,
    textColor=PRIMARY,
    spaceBefore=18,
    spaceAfter=10,
)


HEADING3 = ParagraphStyle(
    "Heading3",
    parent=styles["Heading3"],
    fontName=BOLD_FONT,
    fontSize=14,
    leading=20,
    textColor=PRIMARY_DARK,
    spaceBefore=14,
    spaceAfter=8,
)


# --------------------------------------------------
# Body
# --------------------------------------------------

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName=BODY_FONT,
    fontSize=11,
    leading=18,
    alignment=TA_LEFT,
    textColor=TEXT,
    spaceAfter=8,
)


SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=9,
    leading=13,
    textColor=LIGHT_TEXT,
)


# --------------------------------------------------
# Quote
# --------------------------------------------------

QUOTE = ParagraphStyle(
    "Quote",
    parent=BODY,
    leftIndent=18,
    rightIndent=10,
    borderPadding=10,
    borderColor=BORDER,
    borderWidth=1,
    backColor=colors.HexColor("#F4F8FC"),
    textColor=TEXT,
    italic=True,
)


# --------------------------------------------------
# Code
# --------------------------------------------------

CODE = ParagraphStyle(
    "Code",
    parent=BODY,
    fontName="Courier",
    fontSize=9,
    leading=12,
    leftIndent=10,
    rightIndent=10,
    borderPadding=8,
    backColor=colors.HexColor("#F1F5F9"),
)


# --------------------------------------------------
# Layout
# --------------------------------------------------

PAGE_MARGIN = 0.75 * inch


# --------------------------------------------------
# Tables
# --------------------------------------------------

TABLE_HEADER = PRIMARY

TABLE_ROW = colors.white

TABLE_ALT = colors.HexColor("#F8FAFC")