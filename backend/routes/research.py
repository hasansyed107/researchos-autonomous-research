from io import BytesIO

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from pdf.export import generate_pdf
from services.research import run_research

router = APIRouter()


# ----------------------------------------
# Research Endpoint
# ----------------------------------------

@router.post("/research")
async def research(
    query: str = Form(...),
    file: UploadFile = File(None),
):
    return await run_research(
        query=query,
        file=file,
    )


# ----------------------------------------
# PDF Export
# ----------------------------------------

class PDFRequest(BaseModel):
    topic: str
    report: str


@router.post("/export-pdf")
async def export_pdf(data: PDFRequest):

    pdf_bytes = generate_pdf(
        topic=data.topic,
        report=data.report,
    )

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{data.topic}.pdf"'
        },
    )