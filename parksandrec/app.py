from dash import Dash, dash_table, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import json
import geopandas as gpd
from preprocessing.merge import collapse_tract
from parksandrec.viz import charts

app = Dash(__name__, external_stylesheets= [dbc.themes.COSMO])


data_tract = collapse_tract()

tract_geo = gpd.GeoDataFrame(data_tract, geometry = 'geometry') # REMOVE
tract_geo.set_index('TRACTCE', inplace = True)
geojson_data = json.loads(tract_geo['geometry'].to_json())

tt_cols = tract_geo[['tract','tot_pop', 'avg_hh_size','median_hh_income', 'med_val_own_occ']]

fig_choro = px.choropleth_map(
        title = "Distribution of Open Space in Cook County by Census Tract",
        subtitle = 'Percentage of Land Use assigned to Open Space - 2018',
        data_frame = tract_geo,
        geojson=geojson_data,
        locations= tract_geo.index,
        color =tract_geo["tot_open_space_prop"],
        map_style = 'outdoors',
        zoom = 9,
        color_continuous_scale= 'Viridis',
        center = {'lat': 41.83167, 'lon':-87.67778},
        opacity = 0.7,
        custom_data = ['tract','tot_pop', 'avg_hh_size','median_hh_income', 'med_val_own_occ'],
        labels = {'tot_open_space_prop': "Proportion of open space"},
    )

fig_choro.update_traces(
    hovertemplate =
    "ID: %{customdata[0]}<br>" +
    "Population: %{customdata[1]:,.0f}<br>" + 
    "Avg HH size: %{customdata[2]}<br>" +
    "Median HH Income: %{customdata[3]:$,.0f}<br>" +
    "Median Property Value: %{customdata[4]:$,.0f}<br>"
    "Open Space: %{z:.2%}<br>"+
    "<extra></extra>"
)

fig_choro.update_layout(coloraxis=dict(colorbar=dict(orientation='h', y=-0.20)))

default_graph = charts.plot_income_open_space('tot_open_space_prop', '<', 0.01)

app.layout = [
    html.Div([
        dcc.Graph(
            id='choropleth-map',
            figure=fig_choro,
            style={
                'height': '90vh',
                'width': '60%'
            },
            config={
                'displayModeBar': False
            }
        ),

        html.Div(
            dash_table.DataTable(
                id='race-table',
                data=[]
            )
        )
    ]),
    html.Br(),
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
        html.Br(),
        html.Label("Enter inequality direction: "),
        dcc.RadioItems(
            id = 'direction-radio-button',
            options = [
                {'label': 'less than', 'value': '<'},
                {'label': 'greater than', 'value': '>'}
            ],
            value = '<'
        ),
        html.Br(),
        html.Label("Threshold (percent): "),
        html.Br(),
        dcc.Input(type='number', id='threshold-input', value=10),
        dcc.Graph(figure=default_graph, id='income-graph')
    ], style={'padding': '0px 20px 20px 20px'}),
    
    html.Div([
        html.H2('<Insert title for Landuse graph>'),
        html.Br(),
        html.Img(src=app.get_asset_url('landuse_map.png'), style={'height':'30%', 'width': '60%'}),
        html.Br()
    ])
   
]

@callback(
    Output(component_id='race-table', component_property='data'),
    Input(component_id='choropleth-map', component_property='clickData')
)
def render_race_table(clickData):
    if not clickData:
        return []
    
    tract_id = clickData['points'][0]['location']
    tract_info = data_tract[data_tract['TRACTCE'] == tract_id]
    print(tract_info)

    return tract_info[['white', 'black']].to_dict('records')
    #return json.dumps([tract_info['white'], tract_info['black']])

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
