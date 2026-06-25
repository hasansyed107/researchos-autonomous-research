from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from services.research import (
    run_research
)

router = APIRouter()


@router.post("/research")
async def research(
    query: str = Form(...),
    file: UploadFile = File(None)
):

    return await run_research(
        query=query,
        file=file
    )