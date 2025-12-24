"""Typer CLI application for SWAT-Copilot."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from swat_copilot import __version__
from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.summary import SummarizeService
from swat_copilot.services.analysis import AnalysisService

app = typer.Typer(
    name="swat-copilot",
    help="CLI for SWAT model exploration and analysis",
    add_completion=False,
)
console = Console()

# Global state
project_manager = ProjectManager()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"SWAT-Copilot version {__version__}")


@app.command()
def find(
    search_path: Path = typer.Argument(Path("."), help="Directory to search"),
    max_depth: int = typer.Option(3, help="Maximum search depth"),
) -> None:
    """Find SWAT projects in a directory."""
    console.print(f"Searching for SWAT projects in {search_path}...")

    projects = project_manager.find_projects(search_path, max_depth)

    if not projects:
        console.print("[yellow]No SWAT projects found[/yellow]")
        return

    table = Table(title=f"Found {len(projects)} SWAT Project(s)")
    table.add_column("Path", style="cyan")

    for project_path in projects:
        table.add_row(str(project_path))

    console.print(table)


@app.command()
def load(
    project_path: Path = typer.Argument(..., help="Path to SWAT project"),
) -> None:
    """Load a SWAT project."""
    try:
        console.print(f"Loading project from {project_path}...")
        project = project_manager.load_project(project_path)

        console.print(f"[green]✓[/green] Loaded project: {project.name}")
        console.print(f"  Files: {sum(len(files) for files in project.files.values())}")
        console.print(f"  Has outputs: {project.has_outputs()}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def summary() -> None:
    """Show summary of loaded project."""
    if not project_manager.current_project:
        console.print("[red]No project loaded. Use 'load' command first.[/red]")
        raise typer.Exit(1)

    service = SummarizeService(project_manager.current_project)
    summary_data = service.get_project_summary()

    console.print("\n[bold]Project Summary[/bold]")
    console.print(f"Name: {summary_data['name']}")
    console.print(f"Path: {summary_data['path']}")
    console.print(f"Size: {summary_data['size_mb']} MB")
    console.print(f"Has outputs: {summary_data['has_outputs']}")

    if summary_data.get("file_counts"):
        console.print("\n[bold]File Counts:[/bold]")
        for file_type, count in summary_data["file_counts"].items():
            console.print(f"  {file_type}: {count}")


@app.command()
def outputs() -> None:
    """Show summary of output files."""
    if not project_manager.current_project:
        console.print("[red]No project loaded. Use 'load' command first.[/red]")
        raise typer.Exit(1)

    service = SummarizeService(project_manager.current_project)
    output_summary = service.get_output_summary()

    if not output_summary["has_outputs"]:
        console.print("[yellow]No output files found[/yellow]")
        return

    console.print("\n[bold]Output Files:[/bold]")
    for output in output_summary["output_files"]:
        console.print(f"\n{output['type'].upper()}")
        console.print(f"  Path: {output['path']}")
        if "shape" in output:
            console.print(f"  Shape: {output['shape']}")
            console.print(f"  Variables: {', '.join(output['variables'][:10])}...")


@app.command()
def stats(
    variable: str = typer.Argument(..., help="Variable name"),
    output_type: str = typer.Option("reach", help="Output type (reach/subbasin/hru)"),
    spatial_id: Optional[int] = typer.Option(None, help="Spatial unit ID"),
) -> None:
    """Calculate statistics for a variable."""
    if not project_manager.current_project:
        console.print("[red]No project loaded. Use 'load' command first.[/red]")
        raise typer.Exit(1)

    service = AnalysisService(project_manager.current_project)
    stats_data = service.get_variable_statistics(variable, output_type, spatial_id)

    if "error" in stats_data:
        console.print(f"[red]Error:[/red] {stats_data['error']}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Statistics for {variable}[/bold]")
    console.print(f"Count: {stats_data['count']}")
    console.print(f"Mean: {stats_data['mean']:.2f}")
    console.print(f"Std: {stats_data['std']:.2f}")
    console.print(f"Min: {stats_data['min']:.2f}")
    console.print(f"Max: {stats_data['max']:.2f}")
    console.print(f"Median: {stats_data['median']:.2f}")


@app.command()
def serve_mcp() -> None:
    """Start the MCP server."""
    import asyncio
    from swat_copilot.integrations.mcp.server import SWATMCPServer

    console.print("Starting SWAT MCP Server...")

    async def run_server() -> None:
        server = SWATMCPServer()
        await server.run()

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped[/yellow]")


if __name__ == "__main__":
    app()
