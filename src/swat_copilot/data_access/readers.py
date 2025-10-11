"""Utilities for loading structured SWAT output tables."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_space_table(path: Path, names: list[str]) -> pd.DataFrame:
    """Parse a whitespace delimited table into a DataFrame."""
    text = path.read_text(errors="ignore")
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= len(names):
            rows.append(parts[: len(names)])

    df = pd.DataFrame(rows, columns=names)
    for column in df.columns:
        with pd.option_context("mode.use_inf_as_na", True):
            df[column] = pd.to_numeric(df[column], errors="ignore")
    return df
