"""Token storage for Project Net Zero CLI authentication."""

from __future__ import annotations

from pathlib import Path

TOKEN_DIR = Path.home() / ".projectnetzero"
TOKEN_FILE = TOKEN_DIR / "token"


def save_token(token: str) -> None:
    """Save an authentication token to ~/.projectnetzero/token."""
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token.strip(), encoding="utf-8")


def load_token() -> str | None:
    """Load the saved authentication token, or return None if not found."""
    if not TOKEN_FILE.exists():
        return None
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    return token or None
