from census import Census
from us import states
import pandas as pd
import os

CENSUS_KEY = os.environ["CENSUS_KEY"]

c = Census(CENSUS_KEY)

vars = ("NAME", 
                                       # combined races included 
                                       'B19013_001E', # median household income
                                       'B02001_001E', # total pop
                                       'B02008_001E', # white
                                       'B02009_001E', # black
                                       'B02010_001E', # american indian, alaska native
                                       'B02011_001E', # asian
                                       'B02012_001E', # native hawaiian/pacific islander
                                       'B02013_001E', # other
                                       'B15003_017E', # high school
                                       'B15003_018E', # ged alternatives
                                       'B15003_022E',  # bachelors
                                       'B18101_001E', # total (w and wo dis)
                                       'B18101_004E', # male under 5 w. disability
                                       'B18101_007E', # male 5-17 w. disability
                                       'B18101_010E', # male 18-34 w.dis
                                       'B18101_013E', # male 35-64 w.dis
                                       'B18101_016E', # male 65-74 w.dis
                                       'B18101_019E', # male 75 over w.dis
                                       'B18101_023E', # female under 5 w.dis
                                       'B18101_026E', # female 5-17 w.dis
                                       'B18101_029E', # female 18-34 w.dis
                                       'B18101_032E', # female 35-64 w. dis
                                       'B18101_035E', # female 65 - 74 w.dis
                                       'B18101_038E', # female 75 over w.dis 
                                       'B01001_003E', # male under 5
                                       'B01001_004E', # male 5-9
                                       'B01001_005E', # male 10-14
                                       'B01001_006E', # male 15-17
                                       'B01001_007E', # male 18-19
                                       'B01001_008E', # male 20
                                       'B01001_009E', # male 21
                                       'B01001_010E',#  male 22-24
                                       'B01001_011E', # male 25-29
                                       'B01001_012E', # male 30-34
                                       'B01001_013E', # male 35-39
                                       'B01001_014E', # male 40-44
                                       'B01001_015E', # male 45-49
                                       'B01001_016E', # male 50-54
                                       'B01001_017E', # male 55-59
                                       'B01001_018E', # male 60-61
                                       'B01001_019E', # male 62-64
                                       'B01001_020E', # male 65-66
                                       'B01001_021E', # male 67-69
                                       'B01001_022E', # male 70-74
                                       'B01001_023E', # male 75-79
                                       'B01001_024E', # male 80-84
                                       'B01001_025E', # male 85 over
                                       'B01001_027E', # fem under 5
                                       'B01001_028E', # fem 5-9
                                       'B01001_029E', # fem 10-14
                                       'B01001_030E', # fem 15-17
                                       'B01001_031E', # fem 18-19
                                       'B01001_032E', # fem 20
                                       'B01001_033E', # fem 21
                                       'B01001_034E', # fem 22 -24
                                       'B01001_035E', # fem 25 - 29
                                       'B01001_036E', # fem 30-34
                                       'B01001_037E', # fem 35-39
                                       'B01001_038E', # fem 40-44
                                       'B01001_039E', # fem 45-49
                                       'B01001_040E', # fem 50 -54
                                       'B01001_041E', # fem 55-59
                                       'B01001_042E', # fem 60-61
                                       'B01001_043E', # fem 62-64
                                       'B01001_044E', # fem 65-66
                                       'B01001_045E', # fem 67 - 69
                                       'B01001_046E', # fem 70 -74
                                       'B01001_047E', # fem 75-79
                                       'B01001_048E', # fem 80-84
                                       'B01001_049E') # fem 85 over

def get_census_data(c, year, vars):
    data = c.acs5.state_county_tract(vars,
                                    state_fips = states.IL.fips, 
                                    county_fips = "031",
                                    tract = "*",
                                    year = year)
    data_pd = pd.DataFrame(data)
    
    data_pd['age_under5'] = data_pd['B01001_003E'] + data_pd['B01001_027E']
    data_pd['age_5-9'] = data_pd['B01001_004E'] + data_pd['B01001_028E']
    data_pd['age_10-14'] = data_pd['B01001_005E'] + data_pd['B01001_029E']
    data_pd['age_15-17'] = data_pd['B01001_006E'] + data_pd['B01001_030E']
    data_pd['age_18-19'] = data_pd['B01001_007E'] + data_pd['B01001_031E']
    data_pd['age_20'] = data_pd['B01001_008E'] + data_pd['B01001_032E']
    data_pd['age_21'] = data_pd['B01001_009E'] + data_pd['B01001_033E']
    data_pd['age_22-24'] = data_pd['B01001_010E'] + data_pd['B01001_034E']
    data_pd['age_25-29'] = data_pd['B01001_011E'] + data_pd['B01001_035E']
    data_pd['age_30-34'] = data_pd['B01001_012E'] + data_pd['B01001_036E']
    data_pd['age_35-39'] = data_pd['B01001_013E'] + data_pd['B01001_037E']
    data_pd['age_40-44'] = data_pd['B01001_014E'] + data_pd['B01001_038E']
    data_pd['age_45-49'] = data_pd['B01001_015E'] + data_pd['B01001_039E']
    data_pd['age_50-54'] = data_pd['B01001_016E'] + data_pd['B01001_040E']
    data_pd['age_55-59'] = data_pd['B01001_017E'] + data_pd['B01001_041E']
    data_pd['age_60-61'] = data_pd['B01001_018E'] + data_pd['B01001_042E']
    data_pd['age_62-64'] = data_pd['B01001_019E'] + data_pd['B01001_043E']
    data_pd['age_65-66'] = data_pd['B01001_020E'] + data_pd['B01001_044E']
    data_pd['age_67-69'] = data_pd['B01001_021E'] + data_pd['B01001_045E']
    data_pd['age_70-74'] = data_pd['B01001_022E'] + data_pd['B01001_046E']
    data_pd['age_75-79'] = data_pd['B01001_023E'] + data_pd['B01001_047E']
    data_pd['age_80-84'] = data_pd['B01001_024E'] + data_pd['B01001_048E']
    data_pd['age_85+'] = data_pd['B01001_025E'] + data_pd['B01001_049E']

    data_pd['dis_under5'] = data_pd['B18101_004E'] + data_pd['B18101_023E']
    data_pd['dis_5-17'] = data_pd['B18101_007E'] + data_pd['B18101_026E']
    data_pd['dis_18-34'] = data_pd['B18101_010E'] + data_pd['B18101_029E']
    data_pd['dis_35-64'] = data_pd['B18101_013E'] + data_pd['B18101_032E']
    data_pd['dis_65-74'] = data_pd['B18101_016E'] + data_pd['B18101_035E']
    data_pd['dis_75+'] = data_pd['B18101_019E'] + data_pd['B18101_038E']

    columns = [column for column in data_pd.columns if column.startswith('B18101')
               or column.startswith('B01001')]
    
    subset = data_pd.drop(columns = columns)
    subset.rename(columns = {'B19013_001E': 'median_hh_income', 
                             'B02001_001E': 'total_pop',
                             'B02008_001E': 'race_white', 
                             'B02009_001E': 'race_black',
                             'B02010_001E': 'race_indian_ native',
                             'B02011_001E': 'race_asian',
                             'B02012_001E': 'race_pacific',
                             'B02013_001E': 'race_other',
                             'B15003_017E': 'edu_high school',
                             'B15003_018E': 'edu_ged_alt',
                             'B15003_022E': 'edu_bachelors'
                             }, 
                             inplace = True)

    return subset