"""File readers for SWAT model input and output files."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from swat_copilot.data_access.schemas import (
    OutputData,
    ReachOutput,
    SubbasinOutput,
    HRUOutput,
)


class SWATFileReader(ABC):
    """Base class for SWAT file readers."""

    def __init__(self, file_path: Path) -> None:
        """
        Initialize reader with file path.

        Args:
            file_path: Path to SWAT file
        """
        self.file_path = file_path
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @abstractmethod
    def read(self) -> Any:
        """Read and parse the file."""
        pass

    def read_lines(self, skip_lines: int = 0) -> list[str]:
        """
        Read file lines.

        Args:
            skip_lines: Number of lines to skip from beginning

        Returns:
            List of file lines
        """
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        return lines[skip_lines:]


class ControlFileReader(SWATFileReader):
    """Reader for SWAT control file (file.cio)."""

    def read(self) -> dict[str, Any]:
        """
        Read control file and extract simulation parameters.

        Returns:
            Dictionary of control parameters
        """
        params: dict[str, Any] = {}

        lines = self.read_lines()
        if len(lines) < 10:
            return params

        # Parse key parameters (structure varies by SWAT version)
        # This is a simplified example - actual parsing depends on format
        params["master_watershed"] = lines[0].strip() if lines else ""
        params["has_snowmelt"] = True  # Would parse from file
        params["has_sediment"] = True  # Would parse from file

        return params


class OutputReader(SWATFileReader):
    """Reader for SWAT output files."""

    def __init__(
        self,
        file_path: Path,
        output_type: str = "reach",
        skip_lines: int = 9,
    ) -> None:
        """
        Initialize output reader.

        Args:
            file_path: Path to output file
            output_type: Type of output (reach, subbasin, hru)
            skip_lines: Number of header lines to skip
        """
        super().__init__(file_path)
        self.output_type = output_type
        self.skip_lines = skip_lines

    def read(self) -> OutputData:
        """
        Read output file into structured data.

        Returns:
            OutputData object with parsed results
        """
        df = self._read_to_dataframe()

        if self.output_type == "reach":
            return ReachOutput(data=df, file_path=self.file_path)
        elif self.output_type == "subbasin":
            return SubbasinOutput(data=df, file_path=self.file_path)
        elif self.output_type == "hru":
            return HRUOutput(data=df, file_path=self.file_path)
        else:
            return OutputData(data=df, file_path=self.file_path)

    def _read_to_dataframe(self) -> pd.DataFrame:
        """
        Read output file into pandas DataFrame.

        Returns:
            DataFrame with output data
        """
        try:
            # Read with flexible whitespace delimiter
            df = pd.read_csv(
                self.file_path,
                sep=r"\s+",
                skiprows=self.skip_lines,
                engine="python",
                encoding="utf-8",
                on_bad_lines="skip",
            )
            return df
        except Exception as e:
            # Return empty DataFrame on error
            print(f"Error reading {self.file_path}: {e}")
            return pd.DataFrame()

    def get_variable(self, var_name: str) -> Optional[pd.Series]:
        """
        Extract a specific variable from output.

        Args:
            var_name: Name of variable to extract

        Returns:
            Series with variable values, or None if not found
        """
        df = self._read_to_dataframe()
        if var_name in df.columns:
            return df[var_name]
        return None

    def get_time_series(
        self,
        var_name: str,
        reach_id: Optional[int] = None,
        hru_id: Optional[int] = None,
    ) -> Optional[pd.Series]:
        """
        Get time series for a specific variable and spatial unit.

        Args:
            var_name: Variable name
            reach_id: Reach identifier (for reach outputs)
            hru_id: HRU identifier (for HRU outputs)

        Returns:
            Time series data or None
        """
        df = self._read_to_dataframe()

        if var_name not in df.columns:
            return None

        # Filter by spatial unit if specified
        if reach_id is not None and "RCH" in df.columns:
            df = df[df["RCH"] == reach_id]
        elif hru_id is not None and "HRU" in df.columns:
            df = df[df["HRU"] == hru_id]

        return df[var_name] if not df.empty else None


class SubbasinFileReader(SWATFileReader):
    """Reader for SWAT subbasin files (.sub)."""

    def read(self) -> dict[str, Any]:
        """
        Read subbasin file.

        Returns:
            Dictionary with subbasin parameters
        """
        params: dict[str, Any] = {}
        lines = self.read_lines()

        # Parse subbasin parameters
        # This is a skeleton - actual implementation depends on format
        params["name"] = self.file_path.stem
        params["area"] = 0.0  # Would parse from file
        params["parameters"] = {}

        return params


class HRUFileReader(SWATFileReader):
    """Reader for SWAT HRU files (.hru)."""

    def read(self) -> dict[str, Any]:
        """
        Read HRU file.

        Returns:
            Dictionary with HRU parameters
        """
        params: dict[str, Any] = {}
        lines = self.read_lines()

        # Parse HRU parameters
        params["name"] = self.file_path.stem
        params["land_use"] = ""  # Would parse from file
        params["soil_type"] = ""  # Would parse from file
        params["slope"] = 0.0  # Would parse from file

        return params
