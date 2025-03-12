import pytest
import geopandas as gpd
from parksandrec.preprocessing.merge import collapse_tract
from shapely.geometry import Polygon
from pyproj import CRS



def test_uniqueness():
    test_df = collapse_tract()
    assert test_df['TRACTCE'].is_unique

def test_geodf():
    test_df = collapse_tract()
    assert isinstance(test_df, gpd.GeoDataFrame)
    for i, row in test_df.iterrows():
        assert isinstance(row['geometry'], Polygon)

def test_crs():
    test_df = collapse_tract()
    assert test_df.crs == CRS("EPSG:4269")

