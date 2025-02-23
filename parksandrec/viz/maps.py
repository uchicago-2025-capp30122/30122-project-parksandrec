import altair as alt
from vega_datasets import data
import pygris

def plot_open_space_density():
    # 1. Cloropleth map at the county level: https://altair-viz.github.io/gallery/choropleth.html
    # They do not have any census tract data, will need to check how to analyze 
    # at that geospatial scale.

    # counties will be replaced with tracts: pygris could be a better option
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    source = data.unemployment.url

    alt.Chart(counties).mark_geoshape().encode(
        color='rate:Q'
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(source, 'id', ['rate'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=300
    )

def plot_open_space():
    """
    From https://altair-viz.github.io/gallery/point_map.html
    Plot the location of all open space in Chicago on a map.
    """

    # airports will be replaced with a dataframe containing the census
    # tract ID and the total population of the tract for each open space parcel
    airports = data.airports()

    # Polygons for open spaces will be passed in through the merged dataframe
    # from merge.py
    states = alt.topo_feature(data.us_10m.url, feature='states')

    # The background will be changed to include only Illinois, and zoomed into
    # Cook County
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=500,
        height=300
    ).project('albersUsa')

    # Open space positions on background
    points = alt.Chart(airports).mark_circle(
        size=10,
        color='steelblue'
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        # This will become ['tract', 'area', 'total_pop']
        tooltip=['name', 'city', 'state']
    )

    background + points