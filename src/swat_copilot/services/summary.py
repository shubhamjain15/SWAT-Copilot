"""Service layer for aggregating SWAT project metadata."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from swat_copilot.core.projects import SWATProject


@dataclass(slots=True)
class ProjectSummary:
    """Container for derived project artefacts."""

    metadata: dict[str, int | str]
    sub_table: pd.DataFrame
    hru_table: pd.DataFrame
    root: Path


def build_project_summary(project_root: Path | str) -> ProjectSummary:
    """Collect key summary information for a SWAT project."""
    project = SWATProject.from_path(project_root)
    metadata = project.summary()
    sub_table = project.read_sub()
    hru_table = project.read_hru()
    return ProjectSummary(metadata=metadata, sub_table=sub_table, hru_table=hru_table, root=project.root)
