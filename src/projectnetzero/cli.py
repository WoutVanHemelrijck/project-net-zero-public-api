"""Project Net Zero CLI - optimize and run Python code with lower CO2 emissions."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from projectnetzero import __version__
from projectnetzero.api import DEFAULT_BASE_URL, ProjectNetZeroAPIError, optimize
from projectnetzero.auth import load_token, save_token
from projectnetzero.runner import run_optimized


@click.group()
@click.version_option(version=__version__, prog_name="projectnetzero")
def main() -> None:
    """Project Net Zero - Optimize your Python code for lower CO2 emissions."""


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--api-url",
    default=DEFAULT_BASE_URL,
    envvar="PROJECTNETZERO_API_URL",
    help="Base URL of the optimization API.",
    show_default=True,
)
def run(file: Path, api_url: str) -> None:
    """Optimize a Python file and run the optimized version.

    The original FILE is never modified.
    """
    token = load_token()
    if not token:
        click.echo("No token found. Run 'projectnetzero login' first.", err=True)
        sys.exit(1)

    source_code = file.read_text(encoding="utf-8")

    click.echo(f"Sending {file} to optimization API at {api_url} ...")

    try:
        optimized_code = optimize(source_code, base_url=api_url, token=token)
    except ProjectNetZeroAPIError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Could not reach API: {exc}", err=True)
        sys.exit(1)

    click.echo("Running optimized version ...\n")
    exit_code = run_optimized(optimized_code, file)
    sys.exit(exit_code)


@main.command()
def login() -> None:
    """Save an authentication token for the Project Net Zero API."""
    token = click.prompt("Enter your API token", hide_input=True)
    if not token.strip():
        click.echo("Token cannot be empty.", err=True)
        sys.exit(1)
    save_token(token)
    click.echo("Token saved successfully.")
