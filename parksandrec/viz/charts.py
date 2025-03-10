import altair as alt
from vega_datasets import data
import plotly.express as px
from parksandrec.preprocessing import merge
import pandas as pd

from parksandrec.preprocessing.merge import merge_data

collapsed_data = merge.collapse_tract()
# TODO: Remove this and add the cleanup code in the acs file
collapsed_data = collapsed_data[collapsed_data["median_hh_income"] > 0]

collapsed_data = collapsed_data.sort_values(by="median_hh_income")
income_bins = [
    min(collapsed_data["median_hh_income"]),
    30000,
    50000,
    70000,
    90000,
    110000,
    130000,
    150000,
    170000,
    190000,
    210000,
    max(collapsed_data["median_hh_income"]),
]
collapsed_data["income_bins"], bins = pd.cut(
    collapsed_data["median_hh_income"], income_bins, ordered=True, retbins=True
)
# Some values were converted to NANs, so we drop them
collapsed_data = collapsed_data.dropna(subset=["income_bins"])
collapsed_data["income_bins"] = collapsed_data["income_bins"].astype(str)

# Prepare data for the plot
max_y = collapsed_data["income_bins"].value_counts().max()
all_income_bins = collapsed_data["income_bins"].unique()


def plot_income_open_space(filter_col, inequality, threshold):
    """
    Calculates the total open space by area for each census tract in df

    Parameters:
        df (Pandas.DataFrame): the merged data
    Returns:
        open_space (Pandas.DataFrame): a DataFrame with census tract ID, total
        open space, and median hh income
    """

    inequalities = {"<": "less than", ">": "greater than", "=": "equal to"}

    open_space_types = {
        "tot_open_space_prop": "Open Space",
        "3100_prop": "Recreational",
        "3200_prop": "Golf Courses",
        "3300_prop": "Conservation Areas",
        "3400_prop": "Private Open Space",
    }

    threshold = threshold / 100 if threshold else 0
    filtered_df = filter_by_threshold(collapsed_data, filter_col, inequality, threshold)
    graph_title = (
        "Median HH income distribution for census tracts with "
        + inequalities[inequality]
        + " "
        + str(threshold * 100)
        + "% "
        + open_space_types[filter_col]
    )
    return plot_income_dist(
        filtered_df, "income_bins", all_income_bins, max_y, graph_title
    )


def filter_by_threshold(
    df, filter_col="tot_open_space_prop", inequality_dir="<", threshold=1
):
    if inequality_dir == "<":
        return df[df[filter_col] < threshold]
    elif inequality_dir == ">":
        return df[df[filter_col] > threshold]
    elif inequality_dir == "=":
        return df[df[filter_col] == threshold]


def plot_income_dist(df, x_var, index_on, max_y, graph_title):
    counts = df[x_var].value_counts().reindex(index_on, fill_value=0)
    plot_df = pd.DataFrame({x_var: counts.index, "count": counts.values})
    fig = px.bar(
        plot_df,
        x="income_bins",
        y="count",
        title=graph_title,
        labels={
            "income_bins": "Median HH Income (Binned)",
            "count": "Number of Census Tracts",
        },
    )
    fig.update_layout(yaxis=dict(range=[0, max_y]), xaxis=dict(tickangle=270))
    return fig
