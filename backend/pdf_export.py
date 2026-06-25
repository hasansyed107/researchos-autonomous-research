from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf(
    report_text,
    filename="report.pdf"
):

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    story = []

    for line in report_text.split("\n"):

        story.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 6)
        )

    doc.build(story)

    return filename