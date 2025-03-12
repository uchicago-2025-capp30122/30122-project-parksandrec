import plotly.express as px
from parksandrec.preprocessing import merge
import pandas as pd


def setup_data(collapsed_data):
    """
    Sets up the collapsed_data dataframe imported from merge.py. This function
    is called once by the dashboard when it is first loaded. Storing the data
    in the global space allows the app to repsond instantaneously to toggles and
    filters that the user applies to the income tool.

    Arguments:
        collapsed_data: The dataframe returned by merge.collapse_tract()

    Returns:
        collapsed_data: the dataframe prepared for use in the dashboard

    """
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
    collapsed_data["income_bins"], _ = pd.cut(
        collapsed_data["median_hh_income"], income_bins, ordered=True, retbins=True
    )
    # Some values were converted to NANs, so we drop them
    collapsed_data = collapsed_data.dropna(subset=["income_bins"])
    collapsed_data["income_bins"] = collapsed_data["income_bins"].astype(str)
    return collapsed_data


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
    """
    Helper function to display the income distribution tool on the dashboard

    Arguments:
        df: The dataframe to read from
        filter_col: The type of open space to filter the distribution for.
            Defaults to total open space
        inequality_dir: less than or greater than. Defaults to less than
        threshold: the percentage of open space area in a census tract to filter
            for. Defaults to 1 percent.

        Returns:
            A filtered dataframe based on the inputs
    """

    if inequality_dir == "<":
        return df[df[filter_col] <= threshold]
    elif inequality_dir == ">":
        return df[df[filter_col] >= threshold]
    elif inequality_dir == "=":
        return df[df[filter_col] == threshold]


def plot_income_dist(df, x_var, index_on, max_y, graph_title):
    """
    A helper function to display the income distribution tool on the dashboard

    Arguments:
        df: The dataframe to use for the plot
        x_var: The variable on the x-axis (here, median hh income bins)
        index_on: The index for the df. Here, all median hh income bins for the
            original df, including ones filtered out by filter_by_threshold
        max_y: The maximum y value from the unfiltered dataset, to keep the graph
            consistent
        graph_title: The title of the plot that changes with the toggles on the
            tool

    Returns:
        A Plotly figure to render on the dashboard
    """
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


# This code runs once when charts.py is first imported into the dashboard.
# Setting up the data once as a global variable initially means that the data
# does not have to be fetched, cleaned and processed with each toggle of the
# dashboard and allows the user to see instantaneous updates instead.

collapsed_data = merge.collapse_tract()
collapsed_data = setup_data(collapsed_data)

# Prepare data for the plot
max_y = collapsed_data["income_bins"].value_counts().max()
all_income_bins = collapsed_data["income_bins"].unique()
