import os
import pandas as pd
import parksandrec.preprocessing.acs as acs
import pygris
from pathlib import Path

current_filepath = Path(__file__).resolve()
lui_file_path = current_filepath.parents[2] / "data" / "parcel_tract_linked_nona.pkl"

CENSUS_KEY = os.getenv("CENSUS_KEY")


def merge_data():
    """

    DEPRECATED

    Merges the ACS socio-demographic data with the LUI on the census
    tract ID.

    Returns:
        A Pandas dataframe with merged ACS-LUI data where each row is a land parcel

    """
    # load ACS data
    acs_data = acs.acs_clean(CENSUS_KEY)

    # rename tracts in ACS data so it matches LUI data
    acs_data = acs_data.rename(columns={"tract": "census_tract_id"})

    # load LUI data
    land_data = pd.read_pickle(lui_file_path)

    # do an "inner" merge
    land_acs_merged = pd.merge(land_data, acs_data, on="census_tract_id", how="inner")

    return land_acs_merged


def collapse_tract():
    """
    Create a tract-level datataset with open space metrics and merge it with
    sociodemographic data from ACS and geospatial objects from pygris.

    Inputs:
        None. All dataset iputs are loaded from other functions.

    Returns:
        full_merge (GeoDataFrame): geodataframe containing census-tract level
        metrics on open space (LUI), sociodemographics (ACS) and geometry objects
        (pygris)
    """
    lui_data = pd.read_pickle(lui_file_path)
    acs_data = acs.acs_clean(CENSUS_KEY)

    il_tracts = pygris.tracts(state="IL", county="031", year=2018, cb=True)
    il_tracts_fil = il_tracts[["TRACTCE", "geometry"]]

    lui_tract = lui_data.pivot_table(
        index="census_tract_id",
        columns="LANDUSE",
        values="Shape__Area",
        aggfunc="sum",
        fill_value=0,
    )

    census_merged = pd.merge(
        lui_tract, acs_data, left_on="census_tract_id", right_on="tract", how="inner"
    )

    lu_codes = [
        "1111",
        "1112",
        "1130",
        "1140",
        "1151",
        "1211",
        "1212",
        "1214",
        "1215",
        "1216",
        "1220",
        "1240",
        "1250",
        "1310",
        "1321",
        "1322",
        "1330",
        "1340",
        "1350",
        "1360",
        "1370",
        "1410",
        "1420",
        "1431",
        "1432",
        "1433",
        "1450",
        "1511",
        "1512",
        "1520",
        "1530",
        "1540",
        "1550",
        "1561",
        "1562",
        "1563",
        "1564",
        "1565",
        "1570",
        "2000",
        "3100",
        "3200",
        "3300",
        "3400",
        "3500",
        "4110",
        "4120",
        "4130",
        "4140",
        "4210",
        "4220",
        "4230",
        "4240",
        "5000",
        "6000",
        "9999",
    ]
    # calculate total area of land parcels
    census_merged["tot_parcel_area"] = census_merged[lu_codes].sum(axis=1)

    # calculate proportion of each land use type

    for lui in lu_codes:
        lu_col = lui + "_prop"
        census_merged[lu_col] = census_merged[lui] / census_merged["tot_parcel_area"]

    # calculate total proportion of open spaces
    census_merged["tot_open_space_prop"] = (
        census_merged["3100_prop"]
        + census_merged["3200_prop"]
        + census_merged["3300_prop"]
        + census_merged["3400_prop"]
        + census_merged["3500_prop"]
    )

    # calculate prop of each open space type out of total open space area
    open_space_prop = ["3100_prop", "3200_prop", "3300_prop", "3400_prop", "3500_prop"]

    for prop in open_space_prop:
        new_col = prop + "_open"
        census_merged[new_col] = (
            census_merged[prop] / census_merged["tot_open_space_prop"]
        )

    cols_to_keep = [
        "NAME",
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
        "other_race",
        "two_or_more_races",
        "under_18",
        "65_over",
        "state",
        "county",
        "tract",
        "18_64",
        "tot_parcel_area",
        "3100_prop",
        "3200_prop",
        "3300_prop",
        "3400_prop",
        "3500_prop",
        "tot_open_space_prop",
        "3100_prop_open",
        "3200_prop_open",
        "3300_prop_open",
        "3400_prop_open",
        "3500_prop_open",
    ]

    census_merged_fil = census_merged[cols_to_keep]

    full_merge = pd.merge(
        il_tracts_fil,
        census_merged_fil,
        left_on="TRACTCE",
        right_on="tract",
        how="inner",
    )

    return full_merge
