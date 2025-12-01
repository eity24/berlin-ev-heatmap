import pandas as pd
import geopandas as gpd
import core.HelperTools as ht

# ----------------------------------------------------------------------------- 
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Makes Streamlit App with Heatmap of Electric Charging Stations and Residents"""
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()

    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations and Residents')

    # --- UI controls in sidebar (eity24) ---
st.sidebar.title("Map Controls")
layer_selection = st.sidebar.radio(
    "Select layer",
    ("Residents", "Charging_Stations"),
    help="Choose which data to show as a choropleth: population or number of chargers."
)



    # Slider to control color intensity (fill opacity)
# Slider to control color intensity (fill opacit
copacity = st.sidebar.slider(
        "Fill opacity",
        min_value=0.2,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Adjust how strong the color fill appears on the map."
    )

# Create a Folium map
m = folium.Map(location=[52.52, 13.40], zoom_start=10)

if layer_selection == "Residents":
        # Create a color map for Residents
        color_map = LinearColormap(
            colors=['yellow', 'red'],
            vmin=dframe2['Einwohner'].min(),
            vmax=dframe2['Einwohner'].max()
        )

        # Add polygons to the map for Residents
        for idx, row in dframe2.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': opacity
                },
                tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
            ).add_to(m)
else:
        # Create a color map for Numbers (Charging Stations)
        color_map = LinearColormap(
            colors=['yellow', 'red'],
            vmin=dframe1['Number'].min(),
            vmax=dframe1['Number'].max()
        )

        # Add polygons to the map for Numbers
        for idx, row in dframe1.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': opacity
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
            ).add_to(m)

 # Add color map to the map
            color_map.add_to(m)

              folium_static(m, width=800, height=600)

