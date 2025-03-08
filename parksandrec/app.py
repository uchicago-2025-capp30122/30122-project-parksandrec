from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import json
import pandas as pd
import pygris

from parksandrec.viz import charts, maps

app = Dash()

il_tracts = pygris.tracts(state = "IL", county = "031", year = 2018, cb = True)
geojson_data = json.loads(il_tracts['geometry'].to_json())

fig = go.Figure(
    go.Choropleth(
        geojson=geojson_data,
        locations=il_tracts.index,
        z=il_tracts['ALAND'],
        colorscale="Viridis",
        zmin=il_tracts['ALAND'].min(),
        zmax=il_tracts['ALAND'].max(),
        marker_line_width=0
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

default_graph = charts.plot_income_open_space('tot_open_space_prop', '<', 0.01)

app.layout = [
    html.Div([
        html.H1("Choropleth Map of Illinois Tracts"),
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
