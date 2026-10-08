import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
from app.models.pollution_report import PollutionReport
from app.routers.reports import router as reports_router


def get_cors_origins() -> list[str]:
    configured_origins = os.getenv("CORS_ORIGINS", "")

    if configured_origins.strip():
        return [
            origin.strip().rstrip("/")
            for origin in configured_origins.split(",")
            if origin.strip()
        ]

    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CleanFlow Ghana API",
    description="API for reporting and prioritizing urban pollution incidents.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "CleanFlow Ghana API",
        "status": "running",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
