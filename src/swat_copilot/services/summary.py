"""Service for generating summaries of SWAT projects."""

from pathlib import Path
from typing import Any

from swat_copilot.core.projects import SWATProject, SWATProjectLocator, SWATFileType
from swat_copilot.data_access.readers import OutputReader, ControlFileReader


class SummarizeService:
    """Generate summaries and metadata for SWAT projects."""

    def __init__(self, project: SWATProject) -> None:
        """
        Initialize summarize service.

        Args:
            project: SWAT project to summarize
        """
        self.project = project

    def get_project_summary(self) -> dict[str, Any]:
        """
        Generate comprehensive project summary.

        Returns:
            Dictionary with project summary information
        """
        summary = {
            "name": self.project.name,
            "path": str(self.project.project_path),
            "description": self.project.description,
            "file_counts": self._count_files_by_type(),
            "has_outputs": self.project.has_outputs(),
            "size_mb": self._calculate_project_size(),
        }

        # Add control file info if available
        control_file = self.project.get_file(SWATFileType.CONTROL)
        if control_file:
            try:
                reader = ControlFileReader(control_file.path)
                summary["control_params"] = reader.read()
            except Exception:
                pass

        return summary

    def get_output_summary(self) -> dict[str, Any]:
        """
        Generate summary of output files.

        Returns:
            Dictionary with output summary
        """
        summary: dict[str, Any] = {
            "has_outputs": False,
            "output_files": [],
            "variables": {},
        }

        if not self.project.has_outputs():
            return summary

        summary["has_outputs"] = True

        # Summarize each output type
        output_types = [
            (SWATFileType.OUTPUT_RCH, "reach"),
            (SWATFileType.OUTPUT_SUB, "subbasin"),
            (SWATFileType.OUTPUT_HRU, "hru"),
        ]

        for file_type, output_type in output_types:
            output_file = self.project.get_file(file_type)
            if output_file:
                try:
                    reader = OutputReader(output_file.path, output_type)
                    data = reader.read()
                    summary["output_files"].append(
                        {
                            "type": output_type,
                            "path": str(output_file.path),
                            "shape": data.shape,
                            "variables": data.variables,
                        }
                    )
                    summary["variables"][output_type] = data.variables
                except Exception as e:
                    summary["output_files"].append(
                        {
                            "type": output_type,
                            "path": str(output_file.path),
                            "error": str(e),
                        }
                    )

        return summary

    def _count_files_by_type(self) -> dict[str, int]:
        """Count files by type."""
        counts = {}
        for file_type, files in self.project.files.items():
            if files:
                counts[file_type.value] = len(files)
        return counts

    def _calculate_project_size(self) -> float:
        """Calculate total project size in MB."""
        total_bytes = 0
        for files in self.project.files.values():
            for file in files:
                total_bytes += file.size
        return round(total_bytes / (1024 * 1024), 2)
