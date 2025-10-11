"""FastAPI application for SWAT-Copilot."""
from __future__ import annotations

from fastapi import FastAPI

from swat_copilot.api.routers import health, summary


def create_app() -> FastAPI:
    app = FastAPI(title="SWAT-Copilot API", version="0.0.1")
    app.include_router(health.router)
    app.include_router(summary.router)
    return app


app = create_app()

__all__ = ["app", "create_app"]
