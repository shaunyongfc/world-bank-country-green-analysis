# This file consists of functions and constants written and accumulated across
# the process of EDA.
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
import datetime
import itertools


indicators_dict = {
    "EN.ATM.GHGT.KT.CE": "Total greenhouse gases in CO2",
    "EG.ELC.RNEW.ZS": "Renewable energy in %",
    "NY.GDP.MKTP.CD": "GDP in USD",
    "NY.GDP.PCAP.CD": "GDP per capita in USD",
    "NY.GDP.PCAP.PP.CD": "GDP per capita in PPP",
    "NY.GDP.PCAP.KD.ZG": "GDP per capita growth in %",
    "SP.POP.TOTL": "Total population"
}


def remove_aggregates(df):
    """
    Removes aggregate entities from the DataFrame.
    """
    aggregates = (
        'Africa Eastern and Southern', 'Africa Western and Central',
        'Arab World', 'Caribbean small states',
        'Central Europe and the Baltics', 'Early-demographic dividend',
        'East Asia & Pacific',
        'East Asia & Pacific (excluding high income)',
        'East Asia & Pacific (IDA & IBRD countries)', 'Euro area',
        'Europe & Central Asia',
        'Europe & Central Asia (excluding high income)',
        'Europe & Central Asia (IDA & IBRD countries)', 'European Union',
        'Fragile and conflict affected situations',
        'Heavily indebted poor countries (HIPC)', 'High income',
        'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only',
        'IDA total', 'Late-demographic dividend',
        'Latin America & Caribbean',
        'Latin America & Caribbean (excluding high income)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Least developed countries: UN classification',
        'Low & middle income', 'Low income', 'Lower middle income',
        'Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Middle East & North Africa (IDA & IBRD countries)',
        'Middle income', 'North America', 'Not classified', 'OECD members',
        'Other small states', 'Pacific island small states',
        'Post-demographic dividend', 'Pre-demographic dividend',
        'Small states', 'South Asia', 'South Asia (IDA & IBRD)',
        'Sub-Saharan Africa', 'Sub-Saharan Africa (excluding high income)',
        'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income',
        'World',
    )
    return df[~df.country.isin(aggregates)]


def get_latest_data(df, column):
    """
    Given DataFrame and column name, collect the latest valid value for specific
    column for each country. Countries without valid values are dropped.
    """
    df_segment = df[["country", "year", column]].dropna()
    drop_indices = []
    for country in df_segment.country:
        max_year = max(df_segment[df_segment.country == country].year)
        drop_indices.append(
            (df_segment.country == country) & (df_segment.year < max_year)
        )
    segment_mask = (sum(drop_indices) == 0)
    df_segment = df_segment[segment_mask]
    df_segment = df_segment.drop("year", axis=1)
    df_segment = df_segment.set_index("country")
    return df_segment


def plot_scatter_pairs(data, x_list, y_list, add_dict=None):
    """
    Given a list of x and a list of y, for each pair of x and y, plot a scatter
    graph with certain default settings. The graph includes all years available.

    data: DataFrame of world bank data
    x_list: A list of parameters for the x axis
    y_list: A list of parameters for the y axis
    add_dict: An additional dictionary for new features if applicable.
    """
    labels_dict = indicators_dict
    if add_dict != None:
        labels_dict = {**labels_dict, **add_dict}
    for x, y in itertools.product(x_list, y_list):
        fig = px.scatter(
            data,
            x=x,
            y=y,
            labels=labels_dict,
            hover_data=["country", "year"],
            opacity=0.5
        )
        fig.show()


def plot_scatter_pairs_latest(data, x_list, y_list, add_dict=None):
    """
    Given a list of x and a list of y, for each pair of x and y, plot a scatter
    graph with certain default settings. The graph only includes the latest
    entry for each country.

    data: DataFrame of world bank data
    x_list: A list of parameters for the x axis
    y_list: A list of parameters for the y axis
    add_dict: An additional dictionary for new features if applicable.
    """
    labels_dict = indicators_dict
    if add_dict != None:
        labels_dict = {**labels_dict, **add_dict}
    for x, y in itertools.product(x_list, y_list):
        data_segment = data[["country", "year", x, y]].dropna()
        drop_indices = []
        for country in data_segment.country:
            max_year = max(data_segment[data_segment.country == country].year)
            drop_indices.append(
                (data_segment.country == country) & \
                (data_segment.year < max_year)
            )
        segment_mask = (sum(drop_indices) == 0)
        data_segment = data_segment[segment_mask]
        fig = px.scatter(
            data_segment,
            x=x,
            y=y,
            labels=labels_dict,
            hover_data=["country", "year"],
            opacity=0.5
        )
        fig.show()
