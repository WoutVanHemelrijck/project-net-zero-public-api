"""Project Net Zero optimization API server (proxy)."""

import os

import httpx
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI(title="Project Net Zero API")

security = HTTPBearer()

OPTIMIZER_URL = os.environ.get(
    "OPTIMIZER_URL", "https://project-net-zero-backend-production.up.railway.app/optimize"
)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validate the Bearer token."""
    token = credentials.credentials
    if token != "token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


@app.post("/optimize")
async def optimize(
    project: UploadFile = File(...),
    entrypoint: str = Form(...),
    _token: str = Depends(verify_token),
) -> Response:
    project_bytes = await project.read()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OPTIMIZER_URL,
                files={"project": ("project.zip", project_bytes, "application/zip")},
                data={"entrypoint": entrypoint},
                timeout=300,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Optimizer unreachable: {exc}")

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Optimizer error: {response.text}",
            )

        return Response(
            content=response.content,
            media_type="application/zip",
        )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
