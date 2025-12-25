"""Summary and analysis endpoints."""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.summary import SummarizeService
from swat_copilot.services.analysis import AnalysisService

router = APIRouter()

# Global project manager (in production, use dependency injection)
project_manager = ProjectManager()


@router.post("/projects/load")
async def load_project(project_path: str) -> dict[str, Any]:
    """
    Load a SWAT project.

    Args:
        project_path: Path to SWAT project directory

    Returns:
        Project load status
    """
    try:
        project = project_manager.load_project(Path(project_path))
        return {
            "success": True,
            "project_name": project.name,
            "project_path": str(project.project_path),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/find")
async def find_projects(
    search_path: str = ".",
    max_depth: int = 3,
) -> dict[str, Any]:
    """
    Find SWAT projects in a directory.

    Args:
        search_path: Directory to search
        max_depth: Maximum search depth

    Returns:
        List of found projects
    """
    projects = project_manager.find_projects(Path(search_path), max_depth)
    return {
        "search_path": search_path,
        "projects_found": len(projects),
        "projects": [str(p) for p in projects],
    }


@router.get("/projects/summary")
async def get_project_summary() -> dict[str, Any]:
    """
    Get summary of loaded project.

    Returns:
        Project summary
    """
    if not project_manager.current_project:
        raise HTTPException(status_code=400, detail="No project loaded")

    service = SummarizeService(project_manager.current_project)
    return service.get_project_summary()


@router.get("/projects/outputs/summary")
async def get_output_summary() -> dict[str, Any]:
    """
    Get summary of project outputs.

    Returns:
        Output summary
    """
    if not project_manager.current_project:
        raise HTTPException(status_code=400, detail="No project loaded")

    service = SummarizeService(project_manager.current_project)
    return service.get_output_summary()


@router.get("/analysis/variable/statistics")
async def get_variable_statistics(
    variable: str,
    output_type: str = "reach",
    spatial_id: int | None = None,
) -> dict[str, Any]:
    """
    Get statistics for a variable.

    Args:
        variable: Variable name
        output_type: Output type (reach, subbasin, hru)
        spatial_id: Optional spatial unit ID

    Returns:
        Variable statistics
    """
    if not project_manager.current_project:
        raise HTTPException(status_code=400, detail="No project loaded")

    service = AnalysisService(project_manager.current_project)
    return service.get_variable_statistics(variable, output_type, spatial_id)


@router.get("/analysis/water-balance")
async def calculate_water_balance(output_type: str = "subbasin") -> dict[str, Any]:
    """
    Calculate water balance.

    Args:
        output_type: Output type to use

    Returns:
        Water balance components
    """
    if not project_manager.current_project:
        raise HTTPException(status_code=400, detail="No project loaded")

    service = AnalysisService(project_manager.current_project)
    return service.calculate_water_balance(output_type)
