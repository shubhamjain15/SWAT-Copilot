"""Domain models for interacting with SWAT project directories."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from swat_copilot.data_access.readers import read_space_table


@dataclass(slots=True)
class SWATProject:
    """Representation of a SWAT project on disk."""

    root: Path

    def __post_init__(self) -> None:
        self.root = self.root.resolve()
        if not self.root.exists():
            raise FileNotFoundError(self.root)

    @classmethod
    def from_path(cls, root: Path | str) -> "SWATProject":
        return cls(root=Path(root))

    def read_sub(self) -> pd.DataFrame:
        """Load the SUB basin summary table."""
        table = self.root / "TablesOut" / "sub.txt"
        if table.exists():
            return read_space_table(table, names=["SUB", "AREA_KM2"])

        records: list[dict[str, int | float | None]] = []
        for path in self._iter_files("*.sub"):
            try:
                sub_id = int(path.stem.split(".")[0])
            except ValueError:
                continue
            records.append({"SUB": sub_id, "AREA_KM2": None})

        return pd.DataFrame(records)

    def read_hru(self) -> pd.DataFrame:
        """Return the list of HRU files present in the project."""
        hru_files = list(self._iter_files("*.hru"))
        return pd.DataFrame({"HRU_FILE": [path.name for path in hru_files]})

    def summary(self) -> dict[str, int | str]:
        """Summarise high-level metadata for the project."""
        sub = self.read_sub()
        hru = self.read_hru()
        return {
            "project": self.root.name,
            "n_sub": int(len(sub)) if not sub.empty else 0,
            "n_hru": int(len(hru)) if not hru.empty else 0,
        }

    def _iter_files(self, pattern: str) -> Iterable[Path]:
        return sorted(self.root.glob(pattern))
