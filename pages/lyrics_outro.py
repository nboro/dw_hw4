import math
import json
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from copy import deepcopy

from dash.dependencies import Output, Input

from pages.lyrics import graph_settings

from app import app

# LOAD DATA
with open(f"data/lyric.json", "r") as f:
    all_df = pd.DataFrame.from_dict(json.load(f), orient="index")


# FUNCTIONS
def get_figure(lang, bill_year):
    layout_settings = deepcopy(graph_settings["layout"])
    lyric_df = all_df[(all_df["bill_year"] == bill_year) & all_df.index.str.contains(lang)].copy()
    lyric_agg_df = lyric_df.groupby("era")["pca1", "pca2"].agg(["mean", "std"])
    layout_settings["yaxis"]["range"] = [-0.35, 0.65] if lang == "en" else [-0.15, 0.2]
    layout_settings["xaxis"]["range"] = [-0.5, 0.7] if lang == "en" else [-0.2, 0.2]
    layout_settings["legend"]["title"]["text"] = "Average Era Position"
    traces = []
    shapes = []
    names = {
        "oldies": "1920-1989",
        "90s": "1990-1999",
        "2000s": "2000-2019"
    }
    colors = {
        "oldies": "#f0ad4e",
        "90s": "#5bc0de",
        "2000s": "#d9534f"
    }
    for i, state in enumerate(lyric_agg_df.index.values):
        era_agg_df = lyric_agg_df.loc[state]
        trace = {
            "name": names[state],
            "x": [era_agg_df[("pca1", "mean")]],
            "y": [era_agg_df[("pca2", "mean")]],
            "mode": "markers",
            "text": era_agg_df.index.values,
            "marker": {
                "symbol": "star",
                "color": colors[state],
                "size": 14,
                "opacity": 0.8,
                "line": {
                    "width": 0.5,
                    "color": "#2B3E50"
                }
            },
        }
        traces.append(trace)
        shapes.append({
            "type": "circle",
            "xref": "x",
            "yref": "y",
            "x0": era_agg_df[("pca1", "mean")] - (
                0 if np.isnan(era_agg_df[("pca1", "std")]) else era_agg_df[("pca1", "std")]),
            "x1": era_agg_df[("pca1", "mean")] + (
                0 if np.isnan(era_agg_df[("pca1", "std")]) else era_agg_df[("pca1", "std")]),
            "y0": era_agg_df[("pca2", "mean")] - (
                0 if np.isnan(era_agg_df[("pca2", "std")]) else era_agg_df[("pca2", "std")]),
            "y1": era_agg_df[("pca2", "mean")] + (
                0 if np.isnan(era_agg_df[("pca2", "std")]) else era_agg_df[("pca2", "std")]),
            "opacity": 0.2,
            "fillcolor": colors[state],
            "line": {
                "color": "#2B3E50"
            }
        })
    layout_settings["shapes"] = shapes
    figure = {
        "data": traces,
        "layout": layout_settings
    }
    return dcc.Graph(id="lyric-fig", figure=figure, config=graph_settings["config"])


# CONTENTS
content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Language:"),
                dbc.Select(
                    id="language-dropdown",
                    options=[{"label": "English", "value": "en"}, {"label": "Dutch", "value": "nl"}],
                    value="en"
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Genre:"),
                dbc.Select(
                    id="genre-dropdown",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Rock", "value": "rock"},
                        {"label": "Pop", "value": "pop"},
                        {"label": "Others", "value": "others"},
                    ],
                    value="all",
                    disabled=True
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Search:"),
                dbc.Input(
                    id="search-input",
                    value="",
                    placeholder="Queen, Borsato",
                    type="text",
                    disabled=True
                ),
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col(
            get_figure("en", 1999),
            id="lyric-fig-out",
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label(children="Ranking Year:"),
            dcc.Slider(
                id='ranking-year-slider',
                min=1999,
                max=2019,
                value=1999,
                marks={str(year): str(year) for year in range(1999, 2020)},
                step=None,
                className="custom-range"
            )
        ]),
    ])
]

title = "The Lyric Constellation"

description = html.Div(children=[
    html.H5("Do you find any pattern?", className="text-info"),
    html.H6("Here is what we think about the English song lyrics", className="text-muted"),
    html.P("""
        Based on the distribution, 
        there is no clear distinction between eras but the diversity is interesting to observe. 
        We can see that the songs from before 1990 are more diverse in terms of lyrics.
        This is more apparent in the Rock genre, where Pyscho by Muse is the furthest from the mean, 
        which barely make it to the top 200 in 2016. 
    """),
    html.H6("As for the Dutch songs...", className="text-muted"),
    html.P("""
        The distribution is more polarized, especially between songs before 1990 and the 90s. 
        One in the far left is “Zeg me dat het niet zo is” and in the far right is “De boer dat is de keerl". 
        Wonder what makes these two songs' lyrics so different?
    """)
])


# CALLBACKS
@app.callback(
    Output("lyric-fig-out", "children"),
    [
        Input("language-dropdown", "value"),
        Input("ranking-year-slider", "value")
    ]
)
def display_figure(lang, ranking_year):
    return get_figure(lang, ranking_year)