import altair as alt
from vega_datasets import data

def plot_park_density():
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

