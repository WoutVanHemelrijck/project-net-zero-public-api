"""Run optimized code in a temporary file without modifying the original."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def run_optimized(optimized_code: str, original_path: Path) -> int:
    """Write optimized code to a temp file and execute it.

    The original file is never modified. The temp file is placed in the same
    directory so that relative imports and file paths still work.

    Args:
        optimized_code: The optimized Python source code.
        original_path: Path to the original file (used to resolve the working directory).

    Returns:
        The exit code of the executed process.
    """
    work_dir = original_path.resolve().parent

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        dir=work_dir,
        prefix=".ecofy_",
        delete=True,
    ) as tmp:
        tmp.write(optimized_code)
        tmp.flush()

        result = subprocess.run(
            [sys.executable, tmp.name],
            cwd=work_dir,
        )

    return result.returncode
