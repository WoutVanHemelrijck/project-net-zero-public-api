"""Project Net Zero optimization API server."""

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Project Net Zero API")

OPTIMIZER_URL = "https://web-production-4e9fb.up.railway.app/optimize"


class OptimizeRequest(BaseModel):
    source_code: str


class OptimizeResponse(BaseModel):
    optimized_code: str


@app.post("/optimize")
async def optimize(request: OptimizeRequest) -> OptimizeResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OPTIMIZER_URL,
                json={"source_code": request.source_code},
                timeout=120,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Optimizer unreachable: {exc}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Optimizer error: {response.text}",
        )

    data = response.json()
    return OptimizeResponse(optimized_code=data["optimized_code"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
