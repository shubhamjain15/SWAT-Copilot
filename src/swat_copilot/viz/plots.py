import matplotlib.pyplot as plt
import pandas as pd
def plot_sub_area_hist(df: pd.DataFrame):
   fig, ax = plt.subplots()
   if "AREA_KM2" in df:
       ax.hist(df["AREA_KM2"].dropna())
       ax.set_xlabel("Subbasin Area (km²)")
   else:
       ax.text(0.5, 0.5, "No AREA_KM2 column", ha="center")
   ax.set_ylabel("Count")
   ax.set_title("Subbasin Areas")
   fig.tight_layout()
   return fig
