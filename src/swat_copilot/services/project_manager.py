"""Service for managing SWAT projects."""

from pathlib import Path
from typing import Optional

from swat_copilot.core.projects import SWATProject, SWATProjectLocator
from swat_copilot.config.settings import get_settings


class ProjectManager:
    """Manage SWAT project lifecycle and discovery."""

    def __init__(self) -> None:
        """Initialize project manager."""
        self.settings = get_settings()
        self._current_project: Optional[SWATProject] = None

    @property
    def current_project(self) -> Optional[SWATProject]:
        """Get currently loaded project."""
        return self._current_project

    def load_project(self, project_path: Path) -> SWATProject:
        """
        Load a SWAT project.

        Args:
            project_path: Path to SWAT project directory

        Returns:
            Loaded SWATProject

        Raises:
            ValueError: If path is not a valid SWAT project
        """
        if not SWATProjectLocator.is_swat_project(project_path):
            raise ValueError(f"Not a valid SWAT project: {project_path}")

        # Scan all files in the project
        files = SWATProjectLocator.scan_project_files(project_path)

        # Create project instance
        project = SWATProject(
            project_path=project_path,
            name=project_path.name,
            files=files,
            description=f"SWAT project at {project_path}",
        )

        self._current_project = project
        return project

    def find_projects(
        self,
        search_path: Optional[Path] = None,
        max_depth: int = 3,
    ) -> list[Path]:
        """
        Find SWAT projects under a directory.

        Args:
            search_path: Directory to search (default: current directory or configured default)
            max_depth: Maximum search depth

        Returns:
            List of paths to SWAT projects
        """
        if search_path is None:
            search_path = (
                self.settings.default_swat_project_path
                if self.settings.default_swat_project_path
                else Path.cwd()
            )

        return SWATProjectLocator.find_swat_projects(search_path, max_depth)

    def validate_project(self, project_path: Path) -> dict[str, any]:
        """
        Validate a SWAT project structure.

        Args:
            project_path: Path to validate

        Returns:
            Dictionary with validation results
        """
        results = {
            "is_valid": False,
            "path": str(project_path),
            "errors": [],
            "warnings": [],
        }

        # Check if directory exists
        if not project_path.exists():
            results["errors"].append("Path does not exist")
            return results

        if not project_path.is_dir():
            results["errors"].append("Path is not a directory")
            return results

        # Check for required files
        if not SWATProjectLocator.is_swat_project(project_path):
            results["errors"].append("Missing required SWAT files (file.cio)")
            return results

        results["is_valid"] = True

        # Check for output files
        output_files = list(project_path.glob("output.*"))
        if not output_files:
            results["warnings"].append("No output files found - project may not have been run")

        return results

    def get_project_info(self, project_path: Path) -> dict[str, any]:
        """
        Get quick info about a project without fully loading it.

        Args:
            project_path: Path to project

        Returns:
            Dictionary with basic project info
        """
        info = {
            "path": str(project_path),
            "name": project_path.name,
            "exists": project_path.exists(),
            "is_valid": False,
        }

        if project_path.exists():
            info["is_valid"] = SWATProjectLocator.is_swat_project(project_path)
            files = SWATProjectLocator.scan_project_files(project_path)
            info["file_count"] = sum(len(f) for f in files.values())
            info["has_outputs"] = any(
                ft.value.startswith("output_") for ft in files.keys() if files[ft]
            )

        return info
