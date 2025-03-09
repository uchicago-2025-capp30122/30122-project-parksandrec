from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import json
import geopandas as gpd
from preprocessing.merge import collapse_tract
from parksandrec.viz import charts

app = Dash()

data_tract = collapse_tract()

tract_geo = gpd.GeoDataFrame(data_tract, geometry = 'geometry') # REMOVE
tract_geo.set_index('TRACTCE', inplace = True)
geojson_data = json.loads(tract_geo['geometry'].to_json())

tt_cols = tract_geo[['tract','tot_pop', 'avg_hh_size','median_hh_income', 'med_val_own_occ']]

fig = go.Figure(
    go.Choropleth(
        geojson=geojson_data,
        locations= tract_geo.index,
        z= tract_geo['tot_open_space_prop'],
        colorscale="Viridis",
        zmin=tract_geo['tot_open_space_prop'].min(),
        zmax=tract_geo['tot_open_space_prop'].max(),
        marker_line_width=0,
        customdata = tt_cols,
    )
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    autosize=True,
    geo=dict(
        visible=False,
        showsubunits=True,
        showcountries=False
    ),
    dragmode="zoom",

)
fig.update_traces(
    hovertemplate =
    "ID: %{customdata[0]}<br>" +
    "Population: %{customdata[1]:,.0f}<br>" + 
    "Avg HH size: %{customdata[2]}<br>" +
    "Median HH Income: %{customdata[3]:$,.0f}<br>" +
    "Median Property Value: %{customdata[4]:$,.0f}<br>"
    "Open Space: %{z:.2%}<br>"+
    "<extra></extra>"
)

default_graph = charts.plot_income_open_space('tot_open_space_prop', '<', 0.01)

app.layout = [
    html.Div([
        html.H1("Distribution of Open Space in Cook County by Census Tract"),
        dcc.Graph(
            id='choropleth-map',
            figure=fig,
            style={
                'height': '80vh', 
                'width': '100%'    
            }
        )
    ]),

    html.Div([
        html.Label("Enter open space type: "),
        dcc.Dropdown(
            id = 'open-space-dropdown',
            options = {
                'tot_open_space_prop': 'All',
                '3100_prop': 'Recreational Space',
                '3200_prop': 'Golf Courses',
                '3300_prop': 'Conservation Areas',
                '3400_prop': 'Private Open Space',
                '4110_prop': 'Vacant Residential Land',
                '4120_prop': 'Vacant Commercial Land',
                '4130_prop': 'Vacant Industrial Land'},
            value = 'tot_open_space_prop'
        ),
        html.Label("Enter inequality direction: "),
        dcc.RadioItems(
            id = 'direction-radio-button',
            options = [
                {'label': 'less than', 'value': '<'},
                {'label': 'greater than', 'value': '>'}
            ],
            value = '<'
        ),
        html.Label("Threshold (percent): "),
        dcc.Input(type='number', id='threshold-input', value=10),
        dcc.Graph(figure=default_graph, id='income-graph')
    ])
]

@callback(
    Output(component_id='income-graph', component_property='figure'),
    Input(component_id='open-space-dropdown', component_property='value'),
    Input(component_id='direction-radio-button', component_property='value'),
    Input(component_id='threshold-input', component_property='value'),
)
def update_income_graph(open_space_col, inequality_dir, threshold):
    return charts.plot_income_open_space(open_space_col, inequality_dir, threshold)

if __name__ == '__main__':
    app.run_server(debug=True)
