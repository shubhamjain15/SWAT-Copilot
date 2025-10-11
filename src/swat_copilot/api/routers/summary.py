"""Summary endpoints for SWAT projects."""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Query
from pydantic import BaseModel

from swat_copilot.config.settings import settings
from swat_copilot.services.summary import ProjectSummary, build_project_summary

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectSummaryResponse(BaseModel):
    project: str
    n_sub: int
    n_hru: int
    project_path: str

    @classmethod
    def from_summary(cls, summary: ProjectSummary) -> "ProjectSummaryResponse":
        metadata = summary.metadata
        return cls(
            project=str(metadata.get("project", "")),
            n_sub=int(metadata.get("n_sub", 0)),
            n_hru=int(metadata.get("n_hru", 0)),
            project_path=str(summary.root),
        )


@router.get("/summary", response_model=ProjectSummaryResponse, summary="Project overview")
def project_summary(project: str | None = Query(default=None, description="Path to a SWAT project")) -> ProjectSummaryResponse:
    project_root = Path(project) if project else settings.default_project_root
    summary = build_project_summary(project_root)
    return ProjectSummaryResponse.from_summary(summary)
