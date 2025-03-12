import os
import pandas as pd
from parksandrec.preprocessing.geospatial import get_geodata_2018
import geopandas as gpd
import shapely.geometry
from pathlib import Path
import pytest

# --- Dummy Data Setup --- #

def create_dummy_landuse_gdf():
    """
    Create a dummy landuse GeoDataFrame with two parcels:
    - Row 0: A parcel with a polygon whose centroid falls inside the dummy tract.
    - Row 1: A parcel with a polygon whose centroid falls outside the dummy tract.
    """
    # Parcel 1: inside tract
    inside_polygon = shapely.geometry.Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
    # Parcel 2: outside tract
    outside_polygon = shapely.geometry.Polygon([(20, 20), (21, 20), (21, 21), (20, 21)])
    
    data = {
        'OBJECTID': [1, 2],
        'FIRST_COUNTY': ['031', '031'],
        'LANDUSE': ['1111', '1111'],
        'LANDUSE2': [None, None],
        'OS_MGMT': [None, None],
        'FAC_NAME': [None, None],
        'PLATTED': [None, None],
        'MODIFIER': [None, None],
        'ORIG_FID': [1, 2],
        'Shape__Are': [2827.531250, 3000.0],
        'Shape__Len': [212.932966, 220.0],
        'geometry': [inside_polygon, outside_polygon]
    }
    return gpd.GeoDataFrame(data)


def create_dummy_tracts_gdf():
    """
    Create a dummy tracts GeoDataFrame containing a single tract.
    The tract is a square from (0,0) to (10,10) with COUNTYFP '031'
    and TRACTCE '001', so that it covers the inside parcel.
    """
    tract_polygon = shapely.geometry.Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    data = {
        'STATEFP': ['17'],
        'COUNTYFP': ['031'],
        'TRACTCE': ['001'],
        'AFFGEOID': ['17031000100'],
        'GEOID': ['17031000100'],
        'NAME': ['Dummy Tract'],
        'LSAD': ['CT'],
        'ALAND': [100000],
        'AWATER': [0],
        'geometry': [tract_polygon]
    }
    return gpd.GeoDataFrame(data)

@pytest.fixture
def temp_landuse_file(tmp_path):
    """
    Create a temporary GeoJSON file containing dummy landuse data.
    """
    dummy_gdf = create_dummy_landuse_gdf()
    file_path = tmp_path / "dummy_landuse.geojson"
    dummy_gdf.to_file(file_path, driver="GeoJSON")
    return file_path

@pytest.fixture
def dummy_tracts():
    """
    Returns the dummy tracts GeoDataFrame.
    """
    return create_dummy_tracts_gdf()

# --- Tests --- #

def test_geospatial_pickle_file_exists():
    """
    This test asserts that the pickle file generated by get_geodata_2018 exists
    in the expected location.
    """
    current_filepath = Path(__file__).resolve()
    expected_pickle = current_filepath.parents[1] / "data" / "linked_2018_data.pkl"
    
    assert expected_pickle.exists(), f"Expected pickle file not found at: {expected_pickle}"


def test_geospatial_centroid_identified(temp_landuse_file, dummy_tracts):
    """
    Test that a parcel whose centroid is inside the tract is correctly cataloged.
    """
    dummy_gdf = create_dummy_landuse_gdf().iloc[[0]].copy()
    # Write to a file in the temporary directory.
    file_path = temp_landuse_file.parent / "dummy_inside.geojson"
    dummy_gdf.to_file(file_path, driver="GeoJSON")
    
    # Run the function with the dummy tracts.
    get_geodata_2018(str(file_path), tracts_dummy=dummy_tracts)
    
    exp_pickle = Path(__file__).resolve().parents[1] / "data" / "linked_2018_data.pkl"
    result_gdf = pd.read_pickle(str(exp_pickle))
    
    # Expect one matched parcel with census_tract_id '001'.
    assert len(result_gdf) == 1, "Expected one matched parcel."
    assert result_gdf.iloc[0]['census_tract_id'] == '001', "The matched parcel does not have the correct census tract id."
    
    # Cleanup the pickle file.
    os.remove(str(exp_pickle))

def test_geospatial_centroid_dropped(temp_landuse_file, dummy_tracts):
    """
    Test that a parcel whose centroid is outside any tract is dropped.
    """
    dummy_gdf = create_dummy_landuse_gdf().iloc[[1]].copy()
    # Write to a file in the temporary directory.
    file_path = temp_landuse_file.parent / "dummy_outside.geojson"
    dummy_gdf.to_file(file_path, driver="GeoJSON")
    
    # Run the function with the dummy tracts.
    get_geodata_2018(str(file_path), tracts_dummy=dummy_tracts)
    
    # Construct the expected pickle file path
    exp_pickle = Path(__file__).resolve().parents[1] / "data" / "linked_2018_data.pkl"
    result_gdf = pd.read_pickle(str(exp_pickle))
    
    # Since the parcel's centroid is outside the tract, data should be empty.
    assert result_gdf.empty, "Expected no matched parcels, but some were found."
    
    # Cleanup the pickle file.
    os.remove(str(exp_pickle))