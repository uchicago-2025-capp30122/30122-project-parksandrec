import pytest
import unittest
import os
import pandas as pd
from parksandrec.preprocessing import acs

CENSUS_KEY = os.getenv("CENSUS_KEY")


expected_vars = [
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
        'other_race',
        "two_or_more_races",
        "under_18",
        "65_over",
    ]

def test_get_census_basic():
    """
    Tests for following:
    - ACS Data is pandasDF
    - Expected variables are in the ACS data
    """
 
    clean_acs = acs.acs_clean(CENSUS_KEY)

    # ACS data is a pandas df
    assert isinstance(clean_acs, pd.DataFrame)

    # expected vars in df
    for var in expected_vars:
        assert var in clean_acs.columns


def test_acs_clean():
    """
    Tests for whether there are any negative values for relevant
    int variables
    """

    clean_acs = acs.acs_clean(CENSUS_KEY)

    assert not (clean_acs[expected_vars] < 0).any().any()
