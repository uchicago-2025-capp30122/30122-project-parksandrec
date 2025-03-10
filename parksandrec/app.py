from dash import Dash, dash_table, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import json
from preprocessing.merge import collapse_tract
from parksandrec.viz import charts

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])


data_tract = collapse_tract()

geojson_data = json.loads(data_tract["geometry"].to_json())

tt_cols = data_tract[
    ["tract", "tot_pop", "avg_hh_size", "median_hh_income", "med_val_own_occ"]
]

fig_choro = px.choropleth_map(
    title="Distribution of Open Space in Cook County by Census Tract",
    subtitle="Percentage of Land Use assigned to Open Space - 2018",
    data_frame=data_tract,
    geojson=geojson_data,
    locations=data_tract.index,
    color=data_tract["tot_open_space_prop"],
    map_style="outdoors",
    zoom=9,
    color_continuous_scale="Viridis",
    center={"lat": 41.83167, "lon": -87.67778},
    opacity=0.7,
    custom_data=[
        "tract",
        "tot_pop",
        "avg_hh_size",
        "median_hh_income",
        "med_val_own_occ",
    ],
    labels={"tot_open_space_prop": "Proportion of open space"},
)

fig_choro.update_traces(
    hovertemplate="ID: %{customdata[0]}<br>"
    + "Population: %{customdata[1]:,.0f}<br>"
    + "Avg HH size: %{customdata[2]}<br>"
    + "Median HH Income: %{customdata[3]:$,.0f}<br>"
    + "Median Property Value: %{customdata[4]:$,.0f}<br>"
    "Open Space: %{z:.2%}<br>" + "<extra></extra>"
)

fig_choro.update_layout(coloraxis=dict(colorbar=dict(orientation="h", y=-0.20)))

default_graph = charts.plot_income_open_space("tot_open_space_prop", "<", 0.01)

title = dcc.Markdown(
    """
# **ParksAndRec: From Pawnee to Chicago**
"""
)

intro = dcc.Markdown(
    """
### **How is open space distributed across Chicago and Cook County?**


##### Open space can mean parks, trails and conservation areas, which are desirable for recreation, leisure, and weather regulation. However, it can also mean fallow and underdeveloped lands, which could indicate a lack of investment in built up area and infrastructure. The distribution of such spaces can be determined by socioeconomic factors like neighborhood household incomes, race, and age.

##### `ParksAndRec` aggregates the open space in Chicago at the Census tract level and allows you to explore spatial and statistical data to draw inferences about these correlations in 2018.
    """
)
graph1_body = dcc.Markdown(
    """
Open spaces are categorized based on their primary use and characteristics. Each category is distinct and serves a specific purpose:

- *Recreational spaces*: Recreational open spaces with more than 50% combined impervious surface and manicured turf. This category includes botanical gardens and arboreta.

- *Golf courses*: Public golf courses, country clubs, driving ranges, and associated buildings or parking areas.

- *Conservation areas*: Open spaces in a natural state, with less than 50% combined impervious surface or manicured turf. This includes public lands, state-dedicated nature preserves, and privately-run conservation facilities.

- *Non-public spaces*: Privately owned or restricted-access open spaces, such as hunting clubs, scout camps, and private campgrounds. This is not accessible to the general public.

- *Trails or greenways*: Right-of-way areas maintained for recreational activities, such as walking, cycling, or hiking. Connects communities and promotes outdoor activities in a linear, accessible format.

- *Vacant*: Undeveloped land with no agricultural activity or protection as open space. Includes razed properties in urban settings but excludes vacant developed properties with intact buildings or infrastructure.

"""
)

graph2_body = dcc.Markdown(
    """
The **Chicago Metropolitan Agency for Planning (CMAP)** categorizes open spaces into five types: recreational spaces, golf courses, conservation areas, non-public spaces, and trails or greenways. But how are these open spaces distributed across the census tracts of Cook County? And more importantly, which populations have access to them?

Explore the map to see the concentration of open spaces in different areas. Simply hover over a census tract to reveal details such as the proportion of land dedicated to open space and key demographic indicators of the local population.

Click on a tract to view its race composition.

"""
)

graph3_body = dcc.Markdown(
    """
What is the relationship between the median household income in a Census tract and the total area allocated to open space within it? Are golf courses found in richer tracts? What about abandoned or vacant lots? Which income groups have access to trails and conservation areas?

This tool allows researchers and policymakers to understand how the distribution of income across Cook County changes when controlling for different kinds and amounts of open space. Overall, the trends are complex and related to other demographics like race, historical land use, and city investments, as seen in the map above, but this tool provides a starting point to investigate this complex relationship.

"""
)

about_body = dcc.Markdown(
    '''
Contributors:

- Sarah Hussain
- Raghav Mehrotra
- Jose Maria (Chema) Galvez
- Pablo Hernandez
'''
)

graph1_card = dbc.Card(
    [
        dbc.CardHeader(html.H3("Where is the open space in Cook County?")),
        dbc.CardBody(
            [
                html.H5(graph1_body, className="card-text"),
            ]
        ),
    ]
)

graph3_card = dbc.Card(
    [
        dbc.CardHeader(html.H3("Toggle open spaces to understand income!")),
        dbc.CardBody(
            [
                html.H5(graph3_body, className="card-text"),
            ]
        ),
    ]
)

tab1_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        graph1_card,
                    ],
                    width=5,
                ),
                dbc.Col(
                    html.Img(
                        src=app.get_asset_url("landuse_map.png"),
                        style={
                            "width": "100%",
                            "height": "auto",
                            "maxWidth": "700px",
                            "display": "block",
                            "margin": "0 auto",
                        },
                    ),
                    width=7,
                ),
            ]
        )
    ],
    style={"margin": "10px"},
)

tab2_content = html.Div(
    [
        html.Div(
            html.H5(graph2_body),
            style={"margin": "10px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="choropleth-map",
                        figure=fig_choro,
                        style={"height": "90vh"},
                        config={"displayModeBar": False},
                    ),
                    width=8,
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.H5(id="selected_tract", children="None selected"),
                        dash_table.DataTable(
                            id="race-table",
                            data=[],
                            style_cell={
                                "fontFamily": "sans-serif",
                                "fontSize": "16px",
                                "textAlign": "left",
                            },
                        ),
                    ],
                    width=4,
                ),
            ]
        ),
    ]
)

tab3_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([graph3_card], width=5),
                dbc.Col(
                    [
                        html.Label("Enter open space type: "),
                        dcc.Dropdown(
                            id="open-space-dropdown",
                            options={
                                "tot_open_space_prop": "All",
                                "3100_prop": "Recreational Space",
                                "3200_prop": "Golf Courses",
                                "3300_prop": "Conservation Areas",
                                "3400_prop": "Private Open Space",
                            },
                            value="tot_open_space_prop",
                        ),
                        html.Br(),
                        html.Label("Enter inequality direction: "),
                        dcc.RadioItems(
                            id="direction-radio-button",
                            options=[
                                {"label": "less than", "value": "<"},
                                {"label": "greater than", "value": ">"},
                            ],
                            value="<",
                        ),
                        html.Br(),
                        html.Label("Threshold (percent): "),
                        html.Br(),
                        dcc.Input(type="number", id="threshold-input", value=10),
                        dcc.Graph(figure=default_graph, id="income-graph"),
                    ],
                    width=7,
                    style={"padding": "0px 20px 20px 20px"},
                ),
            ]
        )
    ]
)


app.layout = [
    html.Div(
        title,
        style={
            "font-weight": "bold",
            "margin": "10px",
            "backgroundColor": "darkgreen",
            "color": "white",
            "padding": "20px",
        },
    ),
    html.Div(
        intro,
        style={"margin": "10px", "backgroundColor": "lightgray", "padding": "20px"},
    ),
    dbc.Tabs(
        [
            dbc.Tab(
                tab1_content,
                label="Where?",
                tab_id="parcel",
                style={"margin": "10px", "padding": "20px"},
            ),
            dbc.Tab(
                tab2_content,
                label="Who?",
                tab_id="tract",
                style={"margin": "10px", "padding": "20px"},
            ),
            dbc.Tab(
                tab3_content,
                label="Explore",
                tab_id="stats",
                style={"margin": "10px", "padding": "20px"},
            ),
            dbc.Tab(
                html.Div(
                    about_body,
                    style={
                        "margin": "10px",
                        "padding": "20px",
                    },
                ),
                label="About",
            ),
        ],
        style={"margin": "10px"},
    ),
]


@callback(
    Output(component_id="selected_tract", component_property="children"),
    Output(component_id="race-table", component_property="data"),
    Input(component_id="choropleth-map", component_property="clickData"),
)
def render_race_table(clickData):
    if not clickData:
        return " ", []

    tract_id = clickData["points"][0]["customdata"][0]

    tract_header = f"Demographic Composition of Tract {tract_id}"

    tract_info = data_tract[data_tract["TRACTCE"] == tract_id]

    info_long = tract_info[
        ["white", "black", "native", "asian", "native_hawaiian", "two_or_more_races"]
    ].melt(var_name="Race", value_name="Percentage")

    info_long = info_long[info_long["Percentage"] > 0]

    labels = {
        "white": "White",
        "black": "Black or African American",
        "native": "American Indian or Alaska Native",
        "asian": "Asian",
        "native_hawaiian": "Native Hawaiian or Other Pacific Islander",
        "two_or_more_races": "Two or More Races*",
    }

    info_long["Race"] = info_long["Race"].map(labels)

    info_long = info_long.sort_values(by="Percentage", ascending=False)

    return tract_header, info_long.to_dict("records")


@callback(
    Output(component_id="income-graph", component_property="figure"),
    Input(component_id="open-space-dropdown", component_property="value"),
    Input(component_id="direction-radio-button", component_property="value"),
    Input(component_id="threshold-input", component_property="value"),
)
def update_income_graph(open_space_col, inequality_dir, threshold):
    return charts.plot_income_open_space(open_space_col, inequality_dir, threshold)


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
