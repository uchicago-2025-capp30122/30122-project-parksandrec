import geopandas as gpd
from datetime import datetime
import pandas as pd
import pygris
from pathlib import Path


def get_geodata_2018(landuse_path, tracts_dummy=None):
    """
    Performs a geospatial link between land parcel and census tract data. Assigns
    the census tract that contains the centroid of a land parcel.

    Writes to a local file as a Pandas pickle to prevent repeated computation.

    Arguments:
        landuse_path: The filepath of the file containing land parcel data
        tracts_dummy: Variable to help with testing. Is not used in the function
                      per se
    """

    # Load as geopandas
    landuse = gpd.read_file(landuse_path)

    if tracts_dummy is not None:
        tracts = tracts_dummy # Only for testng in tests/test_geospatial_join.py
    else:
        tracts = pygris.tracts(state="IL", county="Cook", year=2018, cb=True)

    # Drop columns not used for analysis. LANDUSE2 is the seondary land use type
    # but we are only focused on the LANDUSE primary land use type variable
    df_landuse = landuse.drop(
        columns=["LANDUSE2", "OS_MGMT", "FAC_NAME", "PLATTED", "MODIFIER", "ORIG_FID"]
    )
    df_tracts = tracts.drop(
        columns=["AWATER", "ALAND", "LSAD", "NAME", "GEOID", "AFFGEOID", "STATEFP"]
    )

    # Only Cook County data and add census tract column
    cook_landuse = df_landuse[df_landuse["FIRST_COUNTY"] == "031"]
    cook_landuse["census_tract_id"] = ""
    cook_tracts = df_tracts[df_tracts["COUNTYFP"] == "031"]

    # Merge datasets:
    for index, parcel in cook_landuse.iterrows():
        try:
            # Get the geometry data for every row
            geom = parcel["geometry"]
            if geom is None or geom.is_empty:
                continue  # If no geometry data, continue
            centroid = parcel["geometry"].centroid  # Compute centroid
        except KeyError as e:
            # Quit the program if a KeyError occurs. This could happen on the
            # 'geometry' key
            print(f"A KeyError occured: {e}")

        match_found = False  # Initiate to later check NAs
        for _, tract in cook_tracts.iterrows():
            try:
                # Check if centroid inside the tract polygon
                tract_polyon = tract["geometry"]
                if tract_polyon.contains(centroid):
                    # If so, add it to the census_tract_id column
                    cook_landuse.loc[index, "census_tract_id"] = tract["TRACTCE"]
                    match_found = True
                    break  # Exit loop once a match is found
            except KeyError as e:
                # Quit the program if a KeyError occurs. This could happen on the
                # 'geometry' key
                print(f"A KeyError occurred: {e}")

        # If no tract contains the centroid, assign a None value
        if not match_found:
            cook_landuse.loc[index, "census_tract_id"] = None

    # Drop all those None values in the same df
    cook_landuse.dropna(subset=["census_tract_id"], how="all", inplace=True)

    # Save locally to prevent repeating this process
    current_filepath = Path(__file__).resolve()
    pickle_name = current_filepath.parents[1] / "data" / "parcel_tract_linked.pkl"
    cook_landuse.to_pickle(pickle_name)


def get_geodata_2013(landuse_path_1, landuse_path_2, tract_path):
    """
    The 2013 land use data was scraped using the code in scraping.py and stored
    locally. The scraping was done in batches and stored in two separate geojson
    files, which need to be merged. Moreover, this data does not have a COUNTYFP
    column and cannot be filtered for Cook County, which is why the code is
    separated into a separate function.

    Post computation, the data is stored locally in a pickle.

    Arguments:
        landuse_path_1: The filepath of the first batch of data scraped in scraping.py
        landuse_path_2: The filepath of the second batch of data scraped in scraping.py
        tract_path: The filepath of the geospatial data for the relevant census tracts
    """

    df_2013_p1 = gpd.read_file(landuse_path_1)
    df_2013_p2 = gpd.read_file(landuse_path_2)
    df_landuse = pd.concat([df_2013_p1, df_2013_p2], axis=0)

    df_tracts = gpd.read_file(tract_path)
    cook_tracts = df_tracts[df_tracts["COUNTYFP"] == "031"]

    # Drop columns not used for analysis.
    df_landuse = df_landuse.drop(columns=["OS_MGMT", "FAC_NAME", "PLATTED", "MODIFIER"])
    cook_tracts = cook_tracts.drop(
        columns=[
            "STATEFP",
            "COUNTYFP",
            "NAME",
            "NAMELSAD",
            "MTFCC",
            "FUNCSTAT",
            "AWATER",
            "ALAND",
            "INTPTLAT",
            "INTPTLON",
            "GEOID",
        ]
    )

    df_landuse["census_tract_id"] = ""

    # Merge datasets
    count = 0
    for index, parcel in df_landuse.iterrows():
        try:
            # Get the geometry data for every row
            geom = parcel["geometry"]
            if geom is None or geom.is_empty:
                continue  # If no geometry data, continue
            centroid = parcel["geometry"].centroid  # Compute centroid
        except KeyError as e:
            print(f"A KeyError occurred: {e}")

        match_found = False  # Initiate to later check NAs
        for _, tract in cook_tracts.iterrows():
            try:
                # Check if centroid inside the tract polygon
                tract_polyon = tract["geometry"]
                if tract_polyon.contains(centroid):
                    # If so, add it to the census_tract_id column
                    df_landuse.loc[index, "census_tract_id"] = tract["TRACTCE"]
                    match_found = True
                    count += 1
                    break  # Exit loop once a match is found
            except KeyError as e:
                print(f"A KeyError occurred: {e}")

        # If no tract contains the centroid, assign a None value
        if not match_found:
            df_landuse.loc[index, "census_tract_id"] = None

    # Drop all those None values in the same df
    df_landuse.dropna(subset=["census_tract_id"], how="all", inplace=True)

    # Save locally to prevent repeating this process
    pickle_name = (
        "../../"
        + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        + "_linked_2013_data.pkl"
    )
    df_landuse.to_pickle(pickle_name)
