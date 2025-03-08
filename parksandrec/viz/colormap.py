import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def plot_landuse_map(df_path):
    """
    Loads parcel data from a pickle file, processes the LANDUSE column to create
    condensed categories, creates a GeoDataFrame, plots the map with custom colors,
    saves the plot as a PNG file, and returns the processed GeoDataFrame.

    Parameters:
        df_path (str): Path to the pickle file containing the DataFrame.
    
    Returns:
        gdf (GeoDataFrame): The processed GeoDataFrame.
    """
    # Load the DataFrame from the pickle file
    df = pd.read_pickle(df_path)
    
    # Create a GeoDataFrame (assumes a 'geometry' column exists)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    
    # Drop unnecessary columns
    gdf.drop(columns=['OBJECTID', 'FIRST_COUNTY', 'Shape__Area', 'Shape__Length'], inplace=True)
    
    # Initialize the condensed landuse column
    gdf['landuse_condendenced'] = ''
    
    # Update the landuse_condendenced column based on the LANDUSE values
    for i, parcel in gdf.iterrows():
        if parcel['LANDUSE'].startswith('31'):
            gdf.loc[i, 'landuse_condendenced'] = 'Open Space_Recreation'
        if parcel['LANDUSE'].startswith('32'):
            gdf.loc[i, 'landuse_condendenced'] = 'Golf'
        if parcel['LANDUSE'].startswith('33'):
            gdf.loc[i, 'landuse_condendenced'] = 'Open Space_Conservation'
        if parcel['LANDUSE'].startswith('34'):
            gdf.loc[i, 'landuse_condendenced'] = 'Open Space_No Public'
        if parcel['LANDUSE'].startswith('35'):
            gdf.loc[i, 'landuse_condendenced'] = 'Greenway'
    
    # Define the specific categories and corresponding colors
    categories = ['Open Space_Recreation', 'Golf', 'Open Space_Conservation',
                  'Open Space_No Public', 'Greenway']
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    # Convert the landuse column to a categorical type with the defined order
    gdf['landuse_condendenced'] = pd.Categorical(gdf['landuse_condendenced'], categories=categories)
    
    # Create a ListedColormap using the defined colors
    cmap = ListedColormap(colors)
    
    # Create the plot with a specified figure size
    fig, ax = plt.subplots(figsize=(25, 25))
    gdf.plot(column='landuse_condendenced',
             categorical=True,
             legend=True,
             ax=ax,
             cmap=cmap,
             missing_kwds={'color': 'gray'},  # Missing values will be gray.
             legend_kwds={'fontsize': 20, 'title_fontsize': 30})
    
    ax.set_title("Map Colored by LANDUSE")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    
    # Save the plot to a PNG file without displaying it
    fig.savefig("color_landuse_map.png", dpi=300)
    plt.close(fig)
    
    return gdf

gdf_processed = plot_landuse_map('/Users/chemagalvez/Downloads/parcel_tract_linked_nona.pkl')
