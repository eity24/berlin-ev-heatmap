
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
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    # ---------- 1) PLZ geodata ----------
    path_geodat_plz = os.path.join("datasets", "geodata_berlin_plz.csv")
    df_geodat_plz = pd.read_csv(path_geodat_plz, sep=";")

    # ---------- 2) Ladesäulen (charging stations) ----------
    path_lstat = os.path.join("datasets", "ladesaeulenregister.csv")
    df_lstat = pd.read_csv(
        path_lstat,
        sep=";",
        encoding="latin1",
        skiprows=10        # উপরের ১০টা meta লাইন বাদ
    )

    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)

    # ---------- 3) Residents (plz_einwohner.csv) ----------
    path_residents = os.path.join("datasets", "plz_einwohner.csv")

    # sep=None + engine="python" --> delimiter নিজে detect করবে
    df_residents = pd.read_csv(path_residents, sep=None, engine="python")

    # কলাম নামগুলো methods.py যেভাবে expect করে, সেভাবে normalize করি
    # (সব lowercase, আগে/পরে space কেটে)
    df_residents.columns = [c.strip().lower() for c in df_residents.columns]
    # এখন কলামগুলো হওয়া উচিত: ['plz','note','einwohner','qkm','lat','lon']

    # শুধু safety হিসেবে check করে নেই – যদি 'plz','einwohner','lat','lon'
    # অন্য case-এ থাকে, তবু rename করে ঠিক করে দিচ্ছি
    rename_map = {}
    for col in df_residents.columns:
        if col.lower() == "plz":
            rename_map[col] = "plz"
        if col.lower() == "einwohner":
            rename_map[col] = "einwohner"
        if col.lower() == "lat":
            rename_map[col] = "lat"
        if col.lower() == "lon":
            rename_map[col] = "lon"
    df_residents = df_residents.rename(columns=rename_map)

    # এখন df_residents এ methods.py এর preprop_resid ঠিক যেভাবে চায় সেই
    # কলামগুলো থাকছে: 'plz','einwohner','lat','lon'
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # ---------- 4) Streamlit app ----------
    m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)

# -----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__": 
    main()
    

