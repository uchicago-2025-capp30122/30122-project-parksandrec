import pandas as pd
import acs, geospatial

def merge_data():
    """
    Merges the ACS socio-demographic data with the geospatial data on the census
    tract ID. 

    acs = get_census_data()
    geo = get_geodata(landuse_filepath, tract_filepath)
    geo.rename(cols={'TRACTCE': 'tract'})

    merged_df = pd.merge(acs, geo, on='tract', how='inner')

    return merged_df
    """
