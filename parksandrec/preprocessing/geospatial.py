import geopandas as gpd
from shapely import Polygon
import pickle

def merge_datasets(landuse_path, tract_path):
    # Load data
    land_use_shapefile_path = landuse_path
    tract_shapefile_path = tract_path

    # Load as geopandas
    gdf_landuse = gpd.read_file(land_use_shapefile_path)
    gdf = gpd.read_file(tract_shapefile_path)

    # Change landuse coordinates
    gdf_landuse = gdf_landuse.to_crs("EPSG:4269")

    gdf_landuse['centroid'] = gdf_landuse['geometry'].centroid

    # Add dummy column before merge
    gdf_landuse['census_tract'] = 0

    # Filter only for cook_county
    cook_county_land = gdf_landuse[gdf_landuse['FIRST_COUN'] == '031'].head(10)
    cook_county_tracts = gdf[gdf['COUNTYFP'] == '031']

    # Merge the datasets
    count = 0
    for _, land_parsel in cook_county_land.iterrows():
        for __, tract in cook_county_tracts.iterrows():
            if tract['geometry'].contains(land_parsel['centroid']):
                cook_county_land['census_tract'] = cook_county_tracts['TRACTCE']
                break

    cook_county_land.to_pickle('../../../merged_df.pkl')

merge_datasets('/Users/chemagalvez/capp/projects/data/2018_Land_Use_Inventory_for_Northeastern_Illinois/2018_Land_Use_Inventory_for_Northeastern_Illinois.shp', 
               '/Users/chemagalvez/capp/projects/data/cb_2018_17_tract_500k/cb_2018_17_tract_500k.shp')