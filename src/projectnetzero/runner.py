"""Run optimized code from an optimized project directory."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run_optimized(optimized_dir: Path, entrypoint: str) -> int:
    """Run the entrypoint script inside the optimized project directory."""
    script = optimized_dir / entrypoint
    if not script.exists():
        print(f"Error: entrypoint not found: {script}", file=sys.stderr)
        return 1

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=optimized_dir,
        )
        return result.returncode
    finally:
        shutil.rmtree(optimized_dir, ignore_errors=True)
