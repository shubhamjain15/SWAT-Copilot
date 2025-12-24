"""Matplotlib-based plotting functions for SWAT data."""

import base64
from io import BytesIO
from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from swat_copilot.core.projects import SWATProject, SWATFileType
from swat_copilot.data_access.readers import OutputReader
from swat_copilot.config.settings import get_settings

matplotlib.use("Agg")  # Non-interactive backend


class SWATPlotter:
    """Generate plots for SWAT model data."""

    def __init__(self, project: SWATProject) -> None:
        """
        Initialize plotter.

        Args:
            project: SWAT project to plot
        """
        self.project = project
        self.settings = get_settings()

        # Set plot style
        try:
            plt.style.use(self.settings.plot_style)
        except Exception:
            pass  # Use default style if specified style not available

    def plot_time_series(
        self,
        variable: str,
        output_type: str = "reach",
        spatial_id: Optional[int] = None,
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> str:
        """
        Create time series plot.

        Args:
            variable: Variable name to plot
            output_type: Output type (reach, subbasin, hru)
            spatial_id: Optional spatial unit ID
            title: Plot title
            save_path: Optional path to save figure

        Returns:
            Base64-encoded PNG image data
        """
        # Get data
        data = self._get_time_series_data(variable, output_type, spatial_id)
        if data is None or data.empty:
            raise ValueError(f"No data found for variable {variable}")

        # Create figure
        fig, ax = plt.subplots(figsize=self.settings.plot_figsize, dpi=self.settings.plot_dpi)

        # Plot time series
        if "DAY" in data.columns:
            # Daily data
            x_data = range(len(data))
            ax.plot(x_data, data[variable], linewidth=1.5)
            ax.set_xlabel("Day")
        elif "MON" in data.columns:
            # Monthly data
            x_data = range(len(data))
            ax.plot(x_data, data[variable], linewidth=2, marker="o", markersize=4)
            ax.set_xlabel("Month")
        else:
            # Generic index
            ax.plot(data[variable], linewidth=1.5)
            ax.set_xlabel("Index")

        ax.set_ylabel(variable)

        if title:
            ax.set_title(title)
        else:
            spatial_label = f" (ID: {spatial_id})" if spatial_id else ""
            ax.set_title(f"{variable} - {output_type.capitalize()}{spatial_label}")

        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save or return
        return self._figure_to_base64(fig, save_path)

    def plot_comparison(
        self,
        variables: list[str],
        output_type: str = "reach",
        spatial_id: Optional[int] = None,
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> str:
        """
        Create comparison plot for multiple variables.

        Args:
            variables: List of variable names
            output_type: Output type
            spatial_id: Optional spatial unit ID
            title: Plot title
            save_path: Optional path to save figure

        Returns:
            Base64-encoded PNG image data
        """
        fig, axes = plt.subplots(
            len(variables),
            1,
            figsize=(self.settings.plot_figsize[0], self.settings.plot_figsize[1] * len(variables)),
            dpi=self.settings.plot_dpi,
            sharex=True,
        )

        if len(variables) == 1:
            axes = [axes]

        for ax, variable in zip(axes, variables):
            data = self._get_time_series_data(variable, output_type, spatial_id)
            if data is not None and not data.empty and variable in data.columns:
                ax.plot(data[variable], linewidth=1.5)
                ax.set_ylabel(variable)
                ax.grid(True, alpha=0.3)
            else:
                ax.text(
                    0.5,
                    0.5,
                    f"No data for {variable}",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                )

        if title:
            fig.suptitle(title)
        else:
            spatial_label = f" (ID: {spatial_id})" if spatial_id else ""
            fig.suptitle(f"Variable Comparison - {output_type.capitalize()}{spatial_label}")

        plt.tight_layout()

        return self._figure_to_base64(fig, save_path)

    def plot_distribution(
        self,
        variable: str,
        output_type: str = "reach",
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> str:
        """
        Create distribution plot (histogram).

        Args:
            variable: Variable name
            output_type: Output type
            title: Plot title
            save_path: Optional path to save figure

        Returns:
            Base64-encoded PNG image data
        """
        data = self._get_output_reader(output_type)
        if data is None:
            raise ValueError(f"No {output_type} output available")

        var_data = data.get_variable(variable)
        if var_data is None:
            raise ValueError(f"Variable {variable} not found")

        fig, ax = plt.subplots(figsize=self.settings.plot_figsize, dpi=self.settings.plot_dpi)

        ax.hist(var_data.dropna(), bins=30, edgecolor="black", alpha=0.7)
        ax.set_xlabel(variable)
        ax.set_ylabel("Frequency")

        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"Distribution of {variable}")

        ax.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()

        return self._figure_to_base64(fig, save_path)

    def plot_scatter(
        self,
        x_variable: str,
        y_variable: str,
        output_type: str = "reach",
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> str:
        """
        Create scatter plot.

        Args:
            x_variable: X-axis variable
            y_variable: Y-axis variable
            output_type: Output type
            title: Plot title
            save_path: Optional path to save figure

        Returns:
            Base64-encoded PNG image data
        """
        data = self._get_output_reader(output_type)
        if data is None:
            raise ValueError(f"No {output_type} output available")

        output_data = data.read()

        if x_variable not in output_data.variables or y_variable not in output_data.variables:
            raise ValueError("One or both variables not found")

        fig, ax = plt.subplots(figsize=self.settings.plot_figsize, dpi=self.settings.plot_dpi)

        x_data = output_data.get_column(x_variable)
        y_data = output_data.get_column(y_variable)

        ax.scatter(x_data, y_data, alpha=0.5)
        ax.set_xlabel(x_variable)
        ax.set_ylabel(y_variable)

        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"{y_variable} vs {x_variable}")

        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        return self._figure_to_base64(fig, save_path)

    def _get_time_series_data(
        self,
        variable: str,
        output_type: str,
        spatial_id: Optional[int] = None,
    ) -> Optional[pd.DataFrame]:
        """Get time series data for a variable."""
        reader = self._get_output_reader(output_type)
        if reader is None:
            return None

        data = reader.read().data

        # Filter by spatial ID if provided
        if spatial_id is not None:
            id_col = {"reach": "RCH", "subbasin": "SUB", "hru": "HRU"}.get(output_type)
            if id_col and id_col in data.columns:
                data = data[data[id_col] == spatial_id]

        return data

    def _get_output_reader(self, output_type: str) -> Optional[OutputReader]:
        """Get output reader for specified type."""
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
            return OutputReader(output_file.path, output_type)
        except Exception:
            return None

    def _figure_to_base64(self, fig: plt.Figure, save_path: Optional[Path] = None) -> str:
        """
        Convert matplotlib figure to base64-encoded PNG.

        Args:
            fig: Matplotlib figure
            save_path: Optional path to save figure

        Returns:
            Base64-encoded PNG data
        """
        # Save to file if requested
        if save_path:
            fig.savefig(save_path, dpi=self.settings.plot_dpi, bbox_inches="tight")

        # Convert to base64
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=self.settings.plot_dpi, bbox_inches="tight")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()

        plt.close(fig)

        return image_base64
