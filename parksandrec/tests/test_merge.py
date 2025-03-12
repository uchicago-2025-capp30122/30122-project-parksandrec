import pytest
import geopandas as gpd
from parksandrec.preprocessing.merge import collapse_tract
from shapely.geometry import Polygon
from pyproj import CRS

@pytest.fixture
def test_df():
    return collapse_tract()

def test_uniqueness(test_df):
    assert test_df['TRACTCE'].is_unique

def test_geodf(test_df):
    assert isinstance(test_df, gpd.GeoDataFrame)
    assert all(isinstance(geom, Polygon) for geom in test_df['geometry'])

def test_crs(test_df):
    assert test_df.crs == CRS("EPSG:4269")

