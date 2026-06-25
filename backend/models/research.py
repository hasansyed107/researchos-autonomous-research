from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    title: str
    report: str
    generated_at: str