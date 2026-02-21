"""Project Net Zero optimization API server."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Project Net Zero API")


class OptimizeRequest(BaseModel):
    source_code: str


class OptimizeResponse(BaseModel):
    optimized_code: str


def optimizer(source_code: str) -> str:
    """Optimize Python source code for lower CO2 emissions.

    TODO: Replace this stub with the actual optimization logic.
    """
    return source_code


@app.post("/optimize")
def optimize(request: OptimizeRequest) -> OptimizeResponse:
    optimized = optimizer(request.source_code)
    return OptimizeResponse(optimized_code=optimized)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
