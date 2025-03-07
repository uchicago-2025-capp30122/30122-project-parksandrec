import os
import sys 
import pandas as pd
from parksandrec.preprocessing import acs, geospatial
import json
import pickle
from pathlib import Path

current_filepath = Path(__file__).resolve()
lui_file_path = current_filepath.parents[3] / "data" / "parcel_tract_linked_nona.pkl"
#lui_file_path = '../../../data/parcel_tract_linked_nona.pkl'

CENSUS_KEY =  os.getenv('CENSUS_KEY')

def merge_data():
    """
    Merges the ACS socio-demographic data with the LUI on the census
    tract ID. 

    Returns: 
        A Pandas dataframe with merged ACS-LUI data where each row is a land parcel

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









