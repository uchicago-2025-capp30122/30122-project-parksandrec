from census import Census
from us import states
import pandas as pd
import os

CENSUS_KEY = os.environ["CENSUS_KEY"]

c = Census(CENSUS_KEY)

data_2018 = c.acs5.state_county_tract(("NAME", 
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
                                       'B01001_010E',# male 22-24
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
                                       'B01001_025E', # 85 over
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
                                       'B01001_049E'), # fem 85 over
                                      states.IL.fips, "031", 
                                      Census.ALL, 
                                      year = 2018)
data_2018 = pd.DataFrame(data_2018)
data_2018