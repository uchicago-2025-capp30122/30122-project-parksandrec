import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import json
import pandas as pd
import pygris

app = dash.Dash(__name__)

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

app.layout = html.Div([
    html.H1("Choropleth Map of Illinois Tracts"),
    dcc.Graph(
        id='choropleth-map',
        figure=fig,
        style={
            'height': '80vh', 
            'width': '100%'    
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
