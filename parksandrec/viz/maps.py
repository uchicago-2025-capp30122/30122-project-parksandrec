import altair as alt
from vega_datasets import data
import pygris

def plot_park_density():
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
