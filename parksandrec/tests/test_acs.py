import pytest 
import os
from parksandrec.preprocessing import acs

CENUS_KEY = os.getenv("CENSUS_KEY")


# def test_get_census_data():
#     # """
#     # Tests that only cook county ACS data being queried
#     # """

#     # acs_df = acs.get_census_data(CENUS_KEY)
    
#     # assert acs_df[""] 




def test_acs_clean():
    """
    Tests for whether there are any negative values for relevant 
    int variables
    """

    clean_acs = acs.acs_clean(CENUS_KEY)
    int_cols = [
      "owner_occ_units",
      "renter_occ_units",
      "med_val_own_occ",
      "avg_hh_size",
      "pop_25_ba",
      "pop_25_hs",
      "pop_disability",
      "median_hh_income",
      "tot_pop",
      "white",
      "black",
      "native",
      "asian",
      "native_hawaiian",
      "two_or_more_races",
      "under_18",
      "65_over",
      "18_64"
      ]
    
    assert not (clean_acs[int_cols] < 0).any().any()



