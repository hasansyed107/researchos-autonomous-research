import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.research import router

app = FastAPI(
    title="ResearchOS API",
    version="1.0.0"
)

# Frontend URL (local by default, overridden in production)
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "status": "running",
        "app": "ResearchOS"
    }