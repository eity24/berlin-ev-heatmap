
currentWorkingDirectory = r"D:\learning\berlingeoeheatmap_project1-main"
#currentWorkingDirectory = "/mount/src/berlingeoheatmap1/"

# -----------------------------------------------------------------------------
import os
print("Current working directory\n" + os.getcwd())

import pandas as pd
from core import methods as m1
from core import HelperTools as ht
from config import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main() -> None:
    """Main entry point for the Streamlit app.

    The app visualizes:
    - Number of residents per postal code (PLZ) in Berlin
    - Number of public charging points per postal code in Berlin
    """

    # ------------------------------------------------------------------
    # 1) Load base geodata for Berlin postal codes (PLZ polygons)
    # ------------------------------------------------------------------
    path_geodat_plz = os.path.join("datasets", "geodata_berlin_plz.csv")
    df_geodat_plz = pd.read_csv(path_geodat_plz, sep=";")

    # ------------------------------------------------------------------
    # 2) Load and preprocess charging station register
    #    Source: Bundesnetzagentur - "List of charging stations (CSV)"
    # ------------------------------------------------------------------
    path_lstat = os.path.join("datasets", "ladesaeulenregister.csv")

    # The file is semicolon-separated, encoded in latin1 and contains
    # about 10 lines of metadata before the header row.
    df_lstat = pd.read_csv(
        path_lstat,
        sep=";",
        encoding="latin1",
        skiprows=10,
    )

    # Preprocess charging station data and aggregate by PLZ
    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)

    # ------------------------------------------------------------------
    # 3) Load and preprocess residents per PLZ (population data)
    # ------------------------------------------------------------------
    path_residents = os.path.join("datasets", "plz_einwohner.csv")

    # Let pandas automatically detect the separator (comma or semicolon)
    df_residents = pd.read_csv(path_residents, sep=None, engine="python")

    # Normalize column names to what preprop_resid expects
    # Expected columns: 'plz', 'einwohner', 'lat', 'lon'
    df_residents.columns = [c.strip().lower() for c in df_residents.columns]

    rename_map = {}
    for col in df_residents.columns:
        if col.lower() == "plz":
            rename_map[col] = "plz"
        elif col.lower() == "einwohner":
            rename_map[col] = "einwohner"
        elif col.lower() == "lat":
            rename_map[col] = "lat"
        elif col.lower() == "lon":
            rename_map[col] = "lon"

    if rename_map:
        df_residents = df_residents.rename(columns=rename_map)

    # Preprocess residents data and attach PLZ geometry
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # ------------------------------------------------------------------
    # 4) Build and display the Streamlit heatmap app
    # ------------------------------------------------------------------
    m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
    
# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__": 
    main()
    

