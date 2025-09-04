from pathlib import Path
import typer
from rich import print
from swat_copilot.io.swat_project import SWATProject
from swat_copilot.viz.plots import plot_sub_area_hist
app = typer.Typer(add_completion=False)
@app.command()
def info(project: Path = typer.Option(..., exists=True, help="Path to SWAT project root")):
   """Show a quick summary of a SWAT project (counts of HRUs, SUBs, etc.)."""
   sp = SWATProject(project)
   meta = sp.summary()
   for k, v in meta.items():
       print(f"[bold]{k}[/]: {v}")
@app.command()
def plot(project: Path, out: Path = Path("data/subarea_hist.png")):
   """Example plot: SUB file sub-area histogram."""
   sp = SWATProject(project)
   df = sp.read_sub()
   fig = plot_sub_area_hist(df)
   out.parent.mkdir(parents=True, exist_ok=True)
   fig.savefig(out, dpi=160)
   print(f"Saved {out}")
if __name__ == "__main__":
   app()
