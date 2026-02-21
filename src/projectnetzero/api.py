"""Client for the Project Net Zero optimization backend API."""

from __future__ import annotations

import io
import tempfile
import zipfile
from pathlib import Path

import httpx

DEFAULT_BASE_URL = "https://web-production-4e0ee.up.railway.app"


class ProjectNetZeroAPIError(Exception):
    """Raised when the optimization API returns an error."""


def _zip_directory(directory: Path) -> bytes:
    """Create an in-memory zip archive of a directory."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file() and "__pycache__" not in file_path.parts:
                zf.write(file_path, file_path.relative_to(directory))
    buf.seek(0)
    return buf.read()


def optimize_project(
    project_dir: Path,
    entrypoint: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    token: str | None = None,
) -> Path:
    """Zip the project, send it for optimization, extract the response.

    Returns the Path to a temporary directory containing the optimized project.
    The caller is responsible for cleanup (or can let the OS handle it).
    """
    url = f"{base_url.rstrip('/')}/optimize"

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    project_zip = _zip_directory(project_dir)

    response = httpx.post(
        url,
        files={"project": ("project.zip", project_zip, "application/zip")},
        data={"entrypoint": entrypoint},
        headers=headers,
        timeout=300,
    )

    if response.status_code != 200:
        raise ProjectNetZeroAPIError(
            f"API returned status {response.status_code}: {response.text}"
        )

    # Extract the returned zip into a temp directory.
    tmp_dir = Path(tempfile.mkdtemp(prefix="projectnetzero_"))
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall(tmp_dir)

    return tmp_dir
