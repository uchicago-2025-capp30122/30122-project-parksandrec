# parksAndRec: Understanding access to Open and Recreational Space in Chicago

## Members

- José María (Chema) Gálvez Enríquez <jmgalvez@uchicago.edu>
- Pablo Hernandez Pedraza <phernandezpedraz@uchicago.edu>
- Raghav Mehrotra <raghavm@uchicago.edu>
- Sarah Hussain <sthussain@uchicago.edu>

## Abstract[^1]

This project seeks to provide a spatial snapshot of open and recreational spaces in Chicago during the early 2010s and the socioeconomic differences of people living in these neighborhoods. We use three datasets from two sources. We integrate the 2010 Land Use Inventory published by the Chicago Metropolitan Agency for Planning (CMAP) with select multi-year aggregate socioeconomic indicators retrieved from the City of Chicago’s Data Portal, spanning the years 2008 through 2012. This integration would be enabled by the use of the 2012 Geographic Boundaries dataset, also published in the City of Chicago’s Data Portal, which contains georeferenced information delimiting neighborhoods in the city. 

First, we will download GeoJSON land use data from the Chicago Metropolitan Agency for Planning (CMAP), which marks land parcels in Chicago with their land use (e.g. open space, housing, etc.) from 2005 and 2018. Second, we download sociodemographic data at the neighborhood level via the Chicago Data Portal API. By linking these two sources of data, we seek to identify trends in open and public space distribution and their relationship to sociodemographic factors. Third, we download a .csv file from the Chicago Data Portal API to map neighborhood socioeconomic data to geospatial attributes so that they can be analyzed alongside georeferenced land use data. 

We will present our findings through a dashboard with graphs detailing the relationship between sociodemographics and open space. We will also produce a heatmap that highlights where in Chicago open spaces have grown and shrunk in Chicago between 2005 and 2018.

### Data Reconciliation Plan
Our three data sources will involve two steps of merging:

First, we will join Data Source #2 and #3 based on the name of the neighborhood (‘COMMUNITY AREA NAME’ from #2, ‘PRI_NEIGH’ from #3) and add the column ‘the_geom’ to dataset 2. The names appear to be similarly structured, but we will convert them to lowercase and remove all spaces before doing this. The merged data at this stage is expected to have 77 entries, one per neighborhood. At this stage, a naive merge on names gave us only 51 entries because the PRI_NEIGH column contains other data too, so this will need to be cleaned before merging or we could try a fuzzy matching library.

Second, we need to merge the above composite data with the land use GeoJSON data. Each land parcel in Data Source #1 (land use) is smaller than a neighborhood, so for each land parcel, we need to check which neighborhood it is contained in. If it falls into multiple neighborhoods, we will assign it to the neighborhood that it most overlaps with. This will be done using the Multipolygon (list of latitude and longitudes) for each land parcel and each neighborhood. We have not attempted this yet, but we will use Geopandas or pyshp to do this.

At this stage, we have a dataset with a land parcel assigned to a neighborhood and its corresponding socioeconomic data (like median income, crowded housing, etc) and can begin the analysis.

### Data Source #1: [Land Use Inventory for Northeastern Illinois 2010](https://datahub.cmap.illinois.gov/datasets/4bee58b2146b467f8a4a7d694bf8105c_0/explore?location=41.877838%2C-87.624517%2C15.85)

This is bulk data that we had downloaded for Milestone 1, but we are now restricting our analysis to 2010 (due to the lack of other comparable data sources).

We tried downloading this data in 2 formats to compare which is easiest: as a shapefile and as a GeoJSON file. Geopandas was unable to open the Shapefile and insisted that the file extension was .shx and not .shp, so we were having trouble with this and have not resolved it at the moment. The GeoJSON download button doesn’t seem to be working for this particular year (2010) at the moment, but we will try this again. The GeoJSON download did work for 2005 and 2018 data, which are similar to each other (and therefore we expect this to be similar to 2010). Based on the 2005 data, we see that the GeoJSON file is a dictionary, where the key “features” has a list of 101304 features, each representing a land parcel. The land use type (feature[“properties”][“LANDUSE”]) and latitude-longitude coordinates (feature[“coordinates”]) of each parcel are stored in this dictionary, which is the data we are interested in. We will extract the relevant data from the 2010 file in the same way.
Like earlier, the main challenge is expected to arise with the data reconciliation, as explained above. The land use data is straightforward to extract from here.
 
### Data Source #2:  Census Data - Selected socioeconomic indicators in Chicago, 2008 – 2012 
API: https://data.cityofchicago.org/resource/kn9c-c2s2.json

We will retrieve data from the Chicago Data Portal using the following API endpoint: https://data.cityofchicago.org/resource/kn9c-c2s2.json 

This dataset provides information for 77 community areas (e.g., Lincoln Park, Hyde Park), meaning it consists of 77 rows—one for each area. The dataset includes 7 columns, representing 6 key socioeconomic indicators and 1 hardship indicator.

The socioeconomic indicators are 

- Percentage of crowded housing units 
- Percentage of households below poverty 
- Percentage unemployed who are aged 16+ 
- Percentage aged 25+ without high school diploma
- Percentage aged under 18 or over 64
- Per capita income

The data covers the period from 2008 to 2012, and we do not observe any missing values or inconsistencies in this dataset.

### Data Source #3: Data Source #3: Chicago Neighborhood Boundaries


We obtained geospatial boundary data from the [City of Chicago Data Portal](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9), specifically the Boundaries-Neighborhoods dataset. Due to unreliable API access, we directly downloaded the CSV file containing 98 rows and 5 columns:
geom: Multipolygon coordinates defining neighborhood boundaries (critical for geospatial visualizations).
pri_neig: Official name of the Chicago community area (used as the ID key for merging).
sec_neigh, shape_area, shape_len: Secondary neighborhood names and geometric metadata.

Key Challenges & Cleaning Needs:
Row Discrepancy: The dataset lists 98 rows despite Chicago having only 77 official community areas. This occurs because lengthy geom multipolygon values span multiple rows.
Merge Issues: Initial attempts to consolidate split rows using pri_neig as the key identified only 51 neighborhoods, highlighting formatting inconsistencies.
Data Integrity: As an official city dataset, we anticipate resolving these issues (e.g., collapsing split rows, standardizing pri_neig values) to align with the expected 77 community areas.

## Project Plan

Project component and work period
 
1. Continuously check Census (specifically ACS) API to check if it is working (*Feb 3 - Feb 8*). Finalise data sources by Feb 8 depending on the API status. (Pablo) 

2. Set up Git branches (*Feb 3 - Feb 8*) (All) 

3. Get data into our project environment (*Feb 3 - Feb 8*) (All)
    - Download bulk data into Github (save as pkl if needed)
    - Write API calls to get relevant data source

4. Data reconciliation (*Feb 3 - Feb 13*) 
    - Cleaning data (e.g. neighborhood names) (*Feb 8 - Feb 13*) (Pablo and Sarah)
    - Merge socioeconomic data to neighborhood geospatial data (Chema and Sarah)
    - Merge land use data to the resulting data from above (identify relevant Python packages, document logic for edge cases) (Raghav and Chema)

5. Write detailed research questions (*Feb 3 - Feb 8*) (All) 

6. Analysis (depending on the research questions we define in Week 5) (*Feb 17 - Feb 23*) – Examples include correlating open space to income, linking open space to house crowding. (Pablo)

7. Prepare schema of analysis tables and mockups of visuals for Milestone 3 deliverable (*Feb 15 - Feb 19*)
    - Heat map of neighborhoods by amount / percent of open space relative to total space (Raghav and Pablo)
    - Graphs and plots visualizing our analysis – e.g. plotting income against percent of open space across Chicago. (Sarah and Chema)

8. Develop dashboard UI appearance and server logic (*Feb 22 - Feb 28*) (All)

9. Finalize project (*March 1 - March 10*)
    - Readme (Pablo)
    - Final document (All) 
    - Annotating code (Raghav)
    - Update project based on feedback and generate final commit (All)

## Questions
1. Are we allowed to use third-party or institutional packages that facilitate API queries to US Census data, like cenpy or census? Do you recommend their use over a more ‘direct’ API request using the tools we have learned in class?

2. We find that for some queries, R and its package `tidycensus` might be more intuitive that the python equivalents. However, we think it is not ideal, and possibly against the course objectives, to use a different language. What are your thoughts? 

3. Could we request your support in navigating some of the issues we have faced in accessing census data? Might it be part of something bigger?

[^1]: Our project’s former approach strongly depended on accessing the US Census data API. We trust that we will soon be able to use the tool, which implies that our abstract would change to more closely reflect this former approach. However, given that we have recently faced issues, we propose an alternative work plan for this milestone in the event that the obstacles persist beyond this week.
