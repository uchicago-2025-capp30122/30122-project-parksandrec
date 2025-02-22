import geopandas as gpd
from shapely import Polygon
import pickle

# Replace with path shapefile
shapefile_path = ''

# Read the shapefile into a GeoDataFrame
gdf_landuse = gpd.read_file(shapefile_path)

# Display the first few rows of the data
gdf_landuse.info()

# Replace with path shapefile
shapefile_path = '/Users/chemagalvez/capp/projects/data/cb_2018_17_tract_500k/cb_2018_17_tract_500k.shp'

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Display the first few rows of the data
gdf.info()

# Change landuse coordinates
gdf_landuse = gdf_landuse.to_crs("EPSG:4269")

gdf_landuse['centroid'] = gdf_landuse['geometry'].centroid

# Add dummy column before merge
gdf_landuse['census_tract'] = 0

# Filter only for cook_county
cook_county_land = gdf_landuse[gdf_landuse['FIRST_COUN'] == '031']
cook_county_tracts = gdf[gdf['COUNTYFP'] == '031']

# Merge the datasets
count = 0
for index, land_parsel in cook_county_land.iterrows():
    for jindex, tract in cook_county_tracts.iterrows():
        if tract['geometry'].contains(land_parsel['centroid']):
            count += 1
            break

