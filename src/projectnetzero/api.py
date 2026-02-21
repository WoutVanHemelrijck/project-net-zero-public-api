"""Client for the Project Net Zero optimization backend API."""

from __future__ import annotations

import httpx

DEFAULT_BASE_URL = "https://web-production-4e0ee.up.railway.app"


class ProjectNetZeroAPIError(Exception):
    """Raised when the optimization API returns an error."""


def optimize(source_code: str, *, base_url: str = DEFAULT_BASE_URL) -> str:
    """Send source code to the backend and return the optimized version.

    Args:
        source_code: The Python source code to optimize.
        base_url: Base URL of the optimization API.

    Returns:
        The optimized Python source code.

    Raises:
        ProjectNetZeroAPIError: If the API returns a non-success status.
    """
    url = f"{base_url.rstrip('/')}/optimize"

    response = httpx.post(
        url,
        json={"source_code": source_code},
        timeout=120,
    )

    if response.status_code != 200:
        raise ProjectNetZeroAPIError(
            f"API returned status {response.status_code}: {response.text}"
        )

    data = response.json()
    return data["optimized_code"]
