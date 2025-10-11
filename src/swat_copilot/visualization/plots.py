"""Visualization helpers for SWAT datasets."""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def plot_sub_area_hist(df: pd.DataFrame) -> Figure:
    """Draw a histogram of sub-basin areas."""
    fig, ax = plt.subplots()
    if "AREA_KM2" in df:
        ax.hist(df["AREA_KM2"].dropna())
        ax.set_xlabel("Subbasin Area (km²)")
    else:
        ax.text(0.5, 0.5, "No AREA_KM2 column", ha="center", transform=ax.transAxes)
    ax.set_ylabel("Count")
    ax.set_title("Subbasin Areas")
    fig.tight_layout()
    return fig
