"""Service for analyzing SWAT model outputs."""

from typing import Optional, Any

import pandas as pd

from swat_copilot.core.projects import SWATProject, SWATFileType
from swat_copilot.data_access.readers import OutputReader
from swat_copilot.data_access.schemas import OutputData


class AnalysisService:
    """Analyze SWAT model outputs and perform calculations."""

    def __init__(self, project: SWATProject) -> None:
        """
        Initialize analysis service.

        Args:
            project: SWAT project to analyze
        """
        self.project = project

    def get_variable_statistics(
        self,
        variable: str,
        output_type: str = "reach",
        spatial_id: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Calculate statistics for a variable.

        Args:
            variable: Variable name
            output_type: Type of output (reach, subbasin, hru)
            spatial_id: Specific reach/subbasin/HRU ID

        Returns:
            Dictionary with statistics
        """
        data = self._get_output_data(output_type)
        if data is None or variable not in data.variables:
            return {"error": f"Variable {variable} not found"}

        series = data.get_column(variable)
        if series is None:
            return {"error": f"Could not extract {variable}"}

        # Filter by spatial ID if provided
        if spatial_id is not None:
            id_col = self._get_id_column(output_type)
            if id_col and id_col in data.data.columns:
                filtered = data.data[data.data[id_col] == spatial_id]
                if not filtered.empty:
                    series = filtered[variable]

        return {
            "variable": variable,
            "count": len(series),
            "mean": float(series.mean()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "median": float(series.median()),
            "q25": float(series.quantile(0.25)),
            "q75": float(series.quantile(0.75)),
        }

    def compare_scenarios(
        self,
        variable: str,
        scenario1_path: str,
        scenario2_path: str,
    ) -> dict[str, Any]:
        """
        Compare a variable between two scenarios.

        Args:
            variable: Variable to compare
            scenario1_path: Path to first scenario output
            scenario2_path: Path to second scenario output

        Returns:
            Dictionary with comparison results
        """
        # This is a skeleton - actual implementation would load both scenarios
        return {
            "variable": variable,
            "scenario1": scenario1_path,
            "scenario2": scenario2_path,
            "difference": {},
            "percent_change": {},
        }

    def calculate_water_balance(self, output_type: str = "subbasin") -> dict[str, Any]:
        """
        Calculate water balance components.

        Args:
            output_type: Output type to use for calculation

        Returns:
            Dictionary with water balance components
        """
        data = self._get_output_data(output_type)
        if data is None:
            return {"error": "No output data available"}

        # Common SWAT variable names (may vary by version)
        var_mapping = {
            "precipitation": ["PRECIP", "PRECIPmm"],
            "surface_runoff": ["SURQ", "SURQmm"],
            "lateral_flow": ["LATQ", "LATQmm"],
            "groundwater": ["GW_Q", "GWQmm"],
            "evapotranspiration": ["ET", "ETmm"],
            "percolation": ["PERC", "PERCmm"],
        }

        balance = {}
        for component, possible_names in var_mapping.items():
            for var_name in possible_names:
                if var_name in data.variables:
                    series = data.get_column(var_name)
                    if series is not None:
                        balance[component] = float(series.sum())
                        break

        return balance

    def get_time_series(
        self,
        variable: str,
        output_type: str = "reach",
        spatial_id: Optional[int] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Get time series data for a variable.

        Args:
            variable: Variable name
            output_type: Output type
            spatial_id: Specific spatial unit ID

        Returns:
            DataFrame with time series or None
        """
        data = self._get_output_data(output_type)
        if data is None or variable not in data.variables:
            return None

        df = data.data.copy()

        # Filter by spatial ID if provided
        if spatial_id is not None:
            id_col = self._get_id_column(output_type)
            if id_col and id_col in df.columns:
                df = df[df[id_col] == spatial_id]

        if df.empty:
            return None

        # Extract relevant columns
        time_cols = ["MON", "YEAR", "DAY"] if "DAY" in df.columns else ["MON", "YEAR"]
        result_cols = time_cols + [variable]
        available_cols = [c for c in result_cols if c in df.columns]

        return df[available_cols] if available_cols else None

    def _get_output_data(self, output_type: str) -> Optional[OutputData]:
        """Get output data for specified type."""
        file_type_map = {
            "reach": SWATFileType.OUTPUT_RCH,
            "subbasin": SWATFileType.OUTPUT_SUB,
            "hru": SWATFileType.OUTPUT_HRU,
        }

        file_type = file_type_map.get(output_type)
        if not file_type:
            return None

        output_file = self.project.get_file(file_type)
        if not output_file:
            return None

        try:
            reader = OutputReader(output_file.path, output_type)
            return reader.read()
        except Exception:
            return None

    def _get_id_column(self, output_type: str) -> Optional[str]:
        """Get the ID column name for output type."""
        mapping = {
            "reach": "RCH",
            "subbasin": "SUB",
            "hru": "HRU",
        }
        return mapping.get(output_type)
