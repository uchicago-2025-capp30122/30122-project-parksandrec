import pytest
import geopandas as gpd
from parksandrec.preprocessing.merge import collapse_tract


def test_geodf():
    test_df = collapse_tract()
    print(type(test_df))
    assert isinstance(test_df, gpd.GeoDataFrame)

