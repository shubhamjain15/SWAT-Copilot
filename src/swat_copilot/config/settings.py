"""Configuration helpers for SWAT-Copilot."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(slots=True)
class Settings:
    default_project_root: Path

    @classmethod
    def load(cls) -> "Settings":
        root = Path(os.environ.get("SWAT_PROJECT_DIR", ".")).resolve()
        return cls(default_project_root=root)


@lru_cache()
def get_settings() -> Settings:
    return Settings.load()


settings = get_settings()

__all__ = ["Settings", "settings", "get_settings"]
