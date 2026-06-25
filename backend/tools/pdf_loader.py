from pypdf import PdfReader


def load_pdf(file):

    pdf = PdfReader(file)

    text = ""

    for page in pdf.pages:

        text += page.extract_text()

    return text