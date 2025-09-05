from pathlib import Path
import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
from swat_copilot.io.swat_project import SWATProject
app = FastAPI(title="SWAT-Copilot API", version="0.0.1")
class ProjectSummary(BaseModel):
   n_sub: int
   n_hru: int
   project_path: str
@app.get("/healthz")
def health() -> dict:
   return {"ok": True}
@app.get("/summary", response_model=ProjectSummary)
def summary(project: str | None = Query(default=None)) -> ProjectSummary:
   project_dir = Path(project) if project else Path(os.environ.get("SWAT_PROJECT_DIR", "."))
   sp = SWATProject(project_dir)
   meta = sp.summary()
   return ProjectSummary(n_sub=meta["n_sub"], n_hru=meta["n_hru"], project_path=str(project_dir))
