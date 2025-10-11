"""Command line interface entry-points for SWAT-Copilot."""
from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from swat_copilot.services.summary import build_project_summary
from swat_copilot.visualization.plots import plot_sub_area_hist

app = typer.Typer(add_completion=False, help="Utilities for inspecting SWAT projects")


@app.command()
def info(project: Path = typer.Argument(..., exists=True, help="Path to a SWAT project")) -> None:
    """Print a short project summary to the console."""
    summary = build_project_summary(project)
    for key, value in summary.metadata.items():
        print(f"[bold]{key}[/]: {value}")


@app.command()
def plot(
    project: Path = typer.Argument(..., exists=True, help="Path to a SWAT project"),
    out: Path = typer.Option(Path("data/subarea_hist.png"), help="Destination image path"),
) -> None:
    """Render an example SUB area histogram."""
    summary = build_project_summary(project)
    fig = plot_sub_area_hist(summary.sub_table)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=160)
    print(f"Saved {out}")


if __name__ == "__main__":
    app()
