from census import Census
from us import states
import pandas as pd
import os

CENSUS_KEY = os.getenv("CENSUS_KEY")

# variables of interest 
vars = (
    "NAME",
    "DP04_0046PE" ,
    "DP04_0047PE",
    "DP04_0089E",
    "DP02_0016E",
    "DP02_0068PE",
    "DP02_0067PE",
    "DP02_0072PE",
    "DP03_0062E",
    "DP05_0001E",
    "DP05_0037PE",
    "DP05_0038PE",
    "DP05_0039PE",
    "DP05_0047PE",
    "DP05_0055PE",
    "DP05_0061PE",
    "DP05_0019PE",
    "DP05_0029PE",

)



def get_census_data(key, year = 2018, vars = vars):
   """
    Creates a Pandas DataFrame containing relevant American Community Survey (ACS) data, 
    aggregated at the census tract level.

    Parameters:
        - key (str): The API key required to access the ACS data.
        - year (int): The year for which ACS data should be queried.
        - vars (list): A list of variable names (as strings) to be retrieved from the ACS.

    Returns:
        - pd.DataFrame: A DataFrame with the requested ACS data, indexed by census tract.
    """
   # query ACS
   census = Census(key)
   data = census.acs5dp.state_county_tract(vars,
                                    state_fips = states.IL.fips, 
                                    county_fips = "031", # cook county
                                    tract = "*",
                                    year = year)
   # convert data to pandas data frame
   data_pd = pd.DataFrame(data)
   # rename columns from ACS format to user-readable
   data_pd.rename(columns = {'DP04_0046PE': 'owner_occ_units', 
                             'DP04_0047PE': 'renter_occ_units',
                             'DP04_0089E': 'med_val_own_occ',
                             'DP02_0016E': 'avg_hh_size',
                             'DP02_0068PE': 'pop_25_ba', 
                             'DP02_0067PE': 'pop_25_hs',
                             'DP02_0072PE': 'pop_disability', 
                             'DP03_0062E': 'median_hh_income',
                             'DP05_0001E': 'tot_pop',
                             'DP05_0037PE': 'white',
                             'DP05_0038PE': 'black',
                             'DP05_0039PE': 'native',
                             'DP05_0047PE': 'asian', 
                             'DP05_0055PE': 'native_hawaiian', 
                             'DP05_0061PE': 'two_or_more_races', 
                             'DP05_0019PE': 'under_18', 
                             'DP05_0029PE': '65_over',
                             }, 
                             inplace = True)
   
   # convert values in age categories to percentages instead of whole numbers
   data_pd['65_over'] = data_pd['65_over']/data_pd['tot_pop']*100
   data_pd["18_64"] = 100 - (data_pd["under_18"] + data_pd["65_over"])

   # replace negative values for int type columns to 0 (negative values a code for missingness)
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
   data_pd[int_cols] = data_pd[int_cols].clip(lower = 0)

   return data_pd