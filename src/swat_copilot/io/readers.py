from __future__ import annotations
from pathlib import Path
import pandas as pd
def read_space_table(path: Path, names: list[str]) -> pd.DataFrame:
   lines = (l for l in path.read_text(errors="ignore").splitlines() if l.strip())
   rows = []
   for ln in lines:
       parts = ln.split()
       if len(parts) >= len(names):
           rows.append(parts[: len(names)])
   df = pd.DataFrame(rows, columns=names)
   for c in df.columns:
       with pd.option_context("mode.use_inf_as_na", True):
           df[c] = pd.to_numeric(df[c], errors="ignore")
   return df
