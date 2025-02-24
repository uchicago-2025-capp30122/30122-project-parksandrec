# ParksAndRec: Understanding Access to Open and Recreational Space in Chicago

## Members

- José María (Chema) Gálvez Enríquez <jmgalvez@uchicago.edu>
- Pablo Hernandez Pedraza <phernandezpedraz@uchicago.edu>
- Raghav Mehrotra <raghavm@uchicago.edu>
- Sarah Hussain <sthussain@uchicago.edu>

## Abstract

This project examines how the spatial distribution of open and recreational spaces in Chicago has changed from 2013 to 2018 as the city has grown and evolved. We ask *where* open space has grown or shrunk in size and *who* has access to it.

We use four datasets from two sources. First, we obtain land use data from the Land Use Inventory produced by the Chicago Metropolitan Agency for Planning (CMAP) in GeoJSON format, corresponding to the 2013 and 2018 survey waves. This data marks land parcels in Chicago with their land use (e.g. open space, housing, etc.). Second, we use 5-year sociodemographic estimates at the census tract level for median household income, age, education, race, and disability status from the 2013 and 2018 waves of the American Community Survey (ACS). We have obtained this data through queries from the U.S Census Bureau API for all tracts in Cook County, IL. 

Using geospatial joins, we link these two sources of data and identify patterns in the distribution of open and public spaces and their relationship to sociodemographic factors, both of which may vary across time. This approach allows us to identify the characteristics of people living in a delimited space, illustrate disparities in access to a specific public good by comparing geographies, and track shifts in decision making that have either mitigated or aggravated these contrasts.   

##  Data Sources
- Data Source #1: Land Use Inventory for Northeastern Illinois 2013
- Data Source #2: Land Use Inventory for Northeastern Illinois 2018
- Data Source #3: 2013 American Community Survey (Access through Census API via `census` package)
- Data Source #4: 2018 American Community Survey (Access through ACS Census API via `census` package). 

Data sources #1 and #2 are geospatial datasets containing land parcels for the City of Chicago. Each parcel has been tagged with a particular land use (e.g. housing, commercial, open space, etc). We download the GeoJSON files as bulk data, which contain latitude and longitude coordinates for each parcel in addition to the land use information.

Data sources #3 and #4 are representative household surveys collected throughout the year, containing one and five-year estimates of relevant socio-demographic characteristics (income, race, age, education, etc.).Given that the sample representativeness of ACS 1-year estimates at the census tract level is limited, the U.S. Census Bureau pools data across 5-year periods to obtain more reliable estimates across disaggregated geographies. This implies that for a given census tract, a 5-year estimate from the 2013 wave of the ACS contains data collected for this unit spanning the five years up until that wave (2009-2013). Likewise, 5-year estimates for 2018 cover the period between 2014 and 2018.     