import altair as alt
from vega_datasets import data


def plot_income_open_space(source):

    """
    Plot amount of open space against the median hh income for a census tract
    Taken from https://altair-viz.github.io/gallery/scatter_linked_table.html
    """

    # The source input is the merged dataframe
    # 
    # The inputs to the graph are two variables: median_hh_income, already in 
    # the merged data and a calculated variable total_open_space, taken by
    # aggregating the open space area for each census tract in the merged data

    # Brush for selection
    brush = alt.selection_interval()

    # Scatter Plot
    points = alt.Chart(source).mark_point().encode(
        x='median_hh_income',
        y='total_open_space',
        color=alt.when(brush).then(alt.value("steelblue")).otherwise(alt.value("grey"))
    ).add_params(brush)

    # Base chart for data tables
    ranked_text = alt.Chart(source).mark_text(align='right').encode(
        y=alt.Y('row_number:O').axis(None)
    ).transform_filter(
        brush
    ).transform_window(
        row_number='row_number()'
    ).transform_filter(
        alt.datum.row_number < 15
    )

    # Data Tables
    horsepower = ranked_text.encode(text='Horsepower:N').properties(
        title=alt.Title(text='Horsepower', align='right')
    )
    mpg = ranked_text.encode(text='Miles_per_Gallon:N').properties(
        title=alt.Title(text='MPG', align='right')
    )
    origin = ranked_text.encode(text='Origin:N').properties(
        title=alt.Title(text='Origin', align='right')
    )
    text = alt.hconcat(horsepower, mpg, origin) # Combine data tables

    # Build chart
    alt.hconcat(
        points,
        text
    ).resolve_legend(
        color="independent"
    ).configure_view(
        stroke=None
    )

def get_total_open_space(df):
    """
    Calculates the total open space by area for each census tract in df

    Parameters:
        df (Pandas.DataFrame): the merged data
    Returns:
        open_space (Pandas.DataFrame): a DataFrame with census tract ID, total
        open space, and median hh income
    """
    pass