# parksAndRec: Understanding access to Open and Recreational Space in Chicago

## Members

- José María Gálvez Enríquez <jmgalvez@uchicago.edu>
- Pablo Hernandez Pedraza <phernandezpedraz@uchicago.edu>
- Raghav Mehrotra <raghavm@uchicago.edu>
- Sarah Hussain <sthussain@uchicago.edu>

## Abstract

This project examines how the spatial distribution of open and recreational spaces in Chicago has changed from 2005 to 2018 as the city has grown and evolved. We ask not only *where* open space has grown or shrunk in size, but also *who* has access to such spaces as they have evolved.

We use four datasets from two sources. First, we will download GeoJSON land use data from the Chicago Metropolitan Agency for Planning (CMAP), which marks land parcels in Chicago with their land use (e.g. open space, housing, etc.) from 2005 and 2018. Second, we will use sociodemographic data from the 2005 and 2018 waves of the American Community Survey (ACS) (queried via the U.S Census Bureau API), which describes race, age, sex, etc. in Chicago at the Census tract level. By linking these two sources of data, we seek to identify trends in open and public space distribution and their relationship to sociodemographic factors. 

We will present our findings through a dashboard with graphs detailing the relationship between sociodemographics and open space. We will also produce a heatmap that highlights where in Chicago open spaces have grown and shrunk in Chicago between 2005 and 2018.

## Preliminary Data Sources

### Data Source #1: [2005 Land Use Inventory for Northeastern Illinois](https://datahub.cmap.illinois.gov/datasets/2be439b2e0e84f58ab219b7baf3feff2_3/about) (City of Chicago open data portal)

This geospatial dataset contains land parcels for the City of Chicago. Each parcel has been tagged with a particular land use (e.g. housing, commercial, open space, etc). We will download the GeoJSON files as bulk data, which contains latitude and longitude coordinates for each parcel in addition to the land use information.

By itself, this dataset helps us spatialize open and recreational spaces in Chicago. However, the primary challenge comes from the layer of sociodemographic analysis. Each land parcel does not have a neat corresponding Census tract ID in this data. We will need to assign each parcel a Census tract ID using the available location information for the parcel to use the corresponding ACS sociodemographic data. It would be important to develop a strategy to assign a Census tract ID for land parcels that overlap with multiple Census tracts.

### Data Source #2: [2018 Land Use Inventory for Northeastern Illinois](https://datahub.cmap.illinois.gov/maps/c7959bd1c0084edba3264099deeaf365/about) (City of Chicago open data portal)

Like dataset #1, we will download this as bulk data from the URL above.
This dataset provides similar opportunities for spatial analysis in Chicago as dataset #1 and similar challenges for data linking and reconciliation with the 2018 ACS sociodemographic data.

### Data Source #3: [2005 American Community Survey](https://www.census.gov/data/developers/data-sets/acs-1year.2018.html#list-tab-843855098) (Access via [ACS API](https://www.census.gov/programs-surveys/acs/data/data-via-api.html)) 

Representative household survey collected throughout the year, containing population estimates that include size of residents and household composition, as well as relevant socio demographic information on housing conditions, race/ethnicity, employment status, and income and vulnerability (poverty, access to social assistance and public services). This will help answer who has access to open spaces in Chicago.

Challenges: 
- The ACS’s sampling representativeness is limited to the county level, which implies a non-negligible level of noise in all census-tract estimates.
- Disaggregation of data at the county-subdivision-level is only available for population clusters with 65,000 or more people.
- Convenience of working with preprocessed aggregates at the tract-level vs. specificity of processing raw data based on desired attributes. 

### Data Source 4: [2018 American Community Survey](https://www.census.gov/data/developers/data-sets/acs-1year.2018.html#list-tab-843855098) (Access via [ACS API](https://www.census.gov/programs-surveys/acs/data/data-via-api.html))

This dataset contains the same socio-demographic characteristics (household size, race, etc) as dataset #3. As a result, it presents similar opportunities and challenges as described above.

## Preliminary Project Plan

The project will involve 5 major steps with tentative assignments for each:

1. Data ingestion: Downloading of GeoJSON bulk data from the URLs, and using the Census API to query the ACS data. [Raghav, Sarah]
2. Data cleaning and standardization: Removal of null/NA/empty values in a consistent and documented manner and other standardization of columns as needed [Raghav, Sarah]
3. Data reconciliation and linkage: Developing a method to assign each land parcel a 2005 or 2018 Census tract ID based on its latitude and longitude coordinates and documenting this for consistent usage. Linking the two data sources based on the Census tract ID for further analysis. [Raghav, Sarah]
4. Data analysis: Answering the questions of sociodemographic access to open spaces in Chicago and analyzing how this has changed between 2005 and 2018. [Jose, Pablo]
5. Data visualization: Producing a dashboard to visualize the analysis conducted and maps to understand the spatial distribution of open space in Chicago in each year. [Jose, Pablo]

## Questions

1. How strict should our data collection be about time-specific consistencies between data sources (i.e. using the data sources from the same year vs. using the most recent year available? Can we use 2001 land use data with the 2005 ACS?) 
2. Is there an inherent obstacle to our project in the fact that socioeconomic and demographic attributes within a space (Census tract) may change at a faster pace than the anthropic uses of that same space (land parcel)?
3. Should we use ACS 5-year estimates in place of ACS yearly data to obtain a broader range of geographically accurate data at the cost of decreased time variability?  
4. Can you point us to some initial Geospatial libraries to begin looking at?
5. Can you point us to statistical/computational methods on how to effectively link data that are not neatly overlapping (land parcels and Census tracts)?
