import geopandas as gpd
from shapely import Polygon
from pathlib import Path
import pickle

def get_geodata(landuse_path, tract_path):
    # Load as geopandas
    landuse = gpd.read_file(landuse_path)
    tracts = gpd.read_file(tract_path)

    # Drop columns in that we will not be using
    df_landuse = landuse.drop(columns=['LANDUSE2', 'OS_MGMT', 'FAC_NAME', 
                                       'PLATTED', 'MODIFIER', 'ORIG_FID']).copy() # Evaluate make a copy
    df_tracts = tracts.drop(columns=['AWATER', 'ALAND', 'LSAD', 'NAME', 
                                     'GEOID', 'AFFGEOID', 'STATEFP']).copy()

    # Only Cook County data and add census tract column
    cook_landuse = df_landuse[df_landuse['FIRST_COUNTY'] == '031']
    cook_landuse['census_tract_id'] = ''
    cook_tracts = df_tracts[df_tracts['COUNTYFP'] == '031']

    # Merge datasets:
    for index, parcel in cook_landuse.iterrows():
        try:
            # Get the geometry data for every row
            geom = parcel['geometry']
            if geom is None or geom.is_empty:
                continue # If no geometry data, continue
            centroid = parcel['geometry'].centroid  # Compute centroid
        except Exception as e:
            continue # If something went wrong, just continue

        match_found = False # Initiate to later check NAs
        for _, tract in cook_tracts.iterrows():
            try:
                # Check if centroid inside the tract polygon
                tract_polyon = tract['geometry']
                if tract_polyon.contains(centroid):
                    # If so, add it to the census_tract_id column
                    cook_landuse.loc[index, 'census_tract_id'] = tract['TRACTCE']
                    match_found = True
                    break  # Exit loop once a match is found
            except Exception as e:
                continue

        # If no tract contains the centroid, assign a None value
        if not match_found:
            cook_landuse.loc[index, 'census_tract_id'] = None
    
    # Drop all those None values in the same df
    cook_landuse.dropna(subset=['census_tract_id'], how='all', inplace=True)

    # Pickle !
    cook_landuse.to_pickle("parcel_tract_linked.pkl")