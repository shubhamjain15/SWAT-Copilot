"""Data schemas for SWAT model data structures."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass
class OutputData:
    """Base class for SWAT output data."""

    data: pd.DataFrame
    file_path: Path

    @property
    def variables(self) -> list[str]:
        """Get list of available variables."""
        return list(self.data.columns)

    @property
    def shape(self) -> tuple[int, int]:
        """Get shape of data (rows, columns)."""
        return self.data.shape

    def get_column(self, column_name: str) -> Optional[pd.Series]:
        """Get a specific column by name."""
        if column_name in self.data.columns:
            return self.data[column_name]
        return None

    def summary(self) -> dict[str, any]:
        """Get summary statistics."""
        return {
            "n_rows": len(self.data),
            "n_columns": len(self.data.columns),
            "columns": list(self.data.columns),
            "file": str(self.file_path),
        }


@dataclass
class ReachOutput(OutputData):
    """SWAT reach output data (output.rch)."""

    def get_reach_ids(self) -> list[int]:
        """Get list of unique reach IDs."""
        if "RCH" in self.data.columns:
            return sorted(self.data["RCH"].unique().tolist())
        return []

    def get_reach_data(self, reach_id: int) -> pd.DataFrame:
        """Get all data for a specific reach."""
        if "RCH" in self.data.columns:
            return self.data[self.data["RCH"] == reach_id]
        return pd.DataFrame()


@dataclass
class SubbasinOutput(OutputData):
    """SWAT subbasin output data (output.sub)."""

    def get_subbasin_ids(self) -> list[int]:
        """Get list of unique subbasin IDs."""
        if "SUB" in self.data.columns:
            return sorted(self.data["SUB"].unique().tolist())
        return []

    def get_subbasin_data(self, subbasin_id: int) -> pd.DataFrame:
        """Get all data for a specific subbasin."""
        if "SUB" in self.data.columns:
            return self.data[self.data["SUB"] == subbasin_id]
        return pd.DataFrame()


@dataclass
class HRUOutput(OutputData):
    """SWAT HRU output data (output.hru)."""

    def get_hru_ids(self) -> list[int]:
        """Get list of unique HRU IDs."""
        if "HRU" in self.data.columns:
            return sorted(self.data["HRU"].unique().tolist())
        return []

    def get_hru_data(self, hru_id: int) -> pd.DataFrame:
        """Get all data for a specific HRU."""
        if "HRU" in self.data.columns:
            return self.data[self.data["HRU"] == hru_id]
        return pd.DataFrame()


@dataclass
class WaterBalanceData:
    """Water balance calculation results."""

    precipitation: float
    surface_runoff: float
    lateral_flow: float
    groundwater_flow: float
    evapotranspiration: float
    percolation: float
    storage_change: float

    @property
    def total_outflow(self) -> float:
        """Calculate total water outflow."""
        return (
            self.surface_runoff
            + self.lateral_flow
            + self.groundwater_flow
            + self.evapotranspiration
        )

    @property
    def balance_error(self) -> float:
        """Calculate water balance error."""
        return self.precipitation - self.total_outflow - self.storage_change
