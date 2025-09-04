from __future__ import annotations
from pathlib import Path
import pandas as pd
from .readers import read_space_table
class SWATProject:
   def __init__(self, root: Path):
       self.root = Path(root).resolve()
       if not self.root.exists():
           raise FileNotFoundError(self.root)
   def read_sub(self) -> pd.DataFrame:
       tab = self.root / "TablesOut" / "sub.txt"
       if tab.exists():
           return read_space_table(tab, names=["SUB", "AREA_KM2"])
       records = []
       for p in sorted(self.root.glob("*.sub")):
           try:
               sub_id = int(p.stem.split(".")[0])
           except Exception:
               continue
           records.append({"SUB": sub_id, "AREA_KM2": None})
       return pd.DataFrame(records)
   def read_hru(self) -> pd.DataFrame:
       hru_files = list(self.root.glob("*.hru"))
       return pd.DataFrame({"HRU_FILE": [p.name for p in hru_files]})
   def summary(self) -> dict:
       sub = self.read_sub()
       hru = self.read_hru()
       return {
           "project": self.root.name,
           "n_sub": int(len(sub)) if not sub.empty else 0,
           "n_hru": int(len(hru)) if not hru.empty else 0,
       }
