import os
import sys 
import pandas as pd
import acs, geospatial
import json
import pickle

lui_file_path = "/Users/sarahhussain/Downloads/parcel_tract_linked_nona.pkl"
CENSUS_KEY = os.environ["CENSUS_KEY"]

def merge_data():
    """
    Merges the ACS socio-demographic data with the LUI on the census
    tract ID. 

    Returns: 
        Merged ACS-LUI data where each row is a land parcel

    """
    
    # load ACS data
    acs_data = acs.get_census_data(CENSUS_KEY)

    # rename tracts in ACS data so it matches LUI data
    acs_data = acs_data.rename(columns={"tract" : "census_tract_id"})
    
    # load LUI data
    land_data = pd.read_pickle(lui_file_path)

    # do an "inner" merge
    land_acs_merged = pd.merge(land_data, acs_data, on="census_tract_id", how="inner")
    
    
    return land_acs_merged

# EDA
data = merge_data()
print(data[['census_tract_id', 'LANDUSE', 'Shape__Area', 'median_hh_income', 'tot_pop']].head())









