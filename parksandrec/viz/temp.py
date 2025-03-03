import os
import sys 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import preprocessing.acs
import json
import geopandas as gpd



CENSUS_KEY = os.environ["CENSUS_KEY"]




def plot_income_open_space():
    with open("/Users/sarahhussain/Downloads/landuse_census_linked.json", 'r') as f:
        logic_dict = json.load(f)
    #logic_dict = json.loads("/Users/sarahhussain/Downloads/landuse_census_linked.json")
    acs_data = preprocessing.acs.get_census_data()

    # Load as geopandas
    gdf_landuse = gpd.read_file("/Users/sarahhussain/Downloads/2018_Land_Use_Inventory_for_Northeastern_Illinois/2018_Land_Use_Inventory_for_Northeastern_Illinois.shp")
    #tracts = gpd.read_file("/Users/sarahhussain/Downloads/cb_2018_17_tract_500k.shp")

    # cook country land use
    #print(gdf_landuse.head())
    df_landuse_cook = gdf_landuse[gdf_landuse['FIRST_COUN'] == '031']

    shape_area_dict = {"720500": 0}
    count = 0
    for tract in logic_dict:
        if tract["census_tract"] == "720500":
            count += 1
            if tract["land_use"] == "3200":
                for parcel in df_landuse_cook.iterrows():
                    if str(parcel[1]["OBJECTID"]) == str(tract["object_id"]):
                        shape_area_dict[tract["census_tract"]] += float(parcel[1]["Shape__Are"])
            if count % 500 == 0:
                print(f"Looked at {count} tracts we are interested in so far")
                
    print(shape_area_dict)
    
plot_income_open_space()








