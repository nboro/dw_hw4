import math
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from copy import deepcopy
from pages.lyrics import graph_settings

from app import app

# LOAD DATA
with open(f"data/lyric.json", "r") as f:
    all_df = pd.DataFrame.from_dict(json.load(f), orient="index")


# FUNCTIONS
def get_figure():
    layout_settings = deepcopy(graph_settings["layout"])
    lyric_df = all_df[all_df.index.str.contains("en")].copy()

    traces = []
    names = {
        "oldies": "1920-1989",
        "90s": "1990-1999",
        "2000s": "2000-2019"
    }
    for i, state in enumerate(["oldies", "90s", "2000s"]):
        trace_df = lyric_df[lyric_df["era"] == state]
        custom_data = [
            (r["title"], r["artists"], r["bill_rank"], r["bill_year"], idx) for idx, r in trace_df.iterrows()
        ]
        trace = {
            "name": names[state],
            "x": trace_df["pca1"],
            "y": trace_df["pca2"],
            "mode": "markers",
            "text": trace_df["song_id"],
            "customdata": custom_data,
            "hovertemplate": "<b>%{customdata[0]}</b><br> %{customdata[1]}<br> "
                             "Rank=%{customdata[2]} (%{customdata[3]})",
            "marker": {
                "symbol": "circle",
                "size": 11,
                "opacity": 0.8,
                "line": {
                    "width": 0.5,
                    "color": "#2B3E50"
                }
            },
        }
        traces.append(trace)

    figure = {
        "data": [],
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
                    value="en",
                    disabled=True
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
            get_figure(),
            id="lyric-fig-col",
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
                className="custom-range",
                disabled=True
            )
        ]),
    ])
]

title = "The Lyric Constellation"

description = html.Div(children=[
    html.H5("Measuring lyric diversity across different genres and song eras", className="text-info"),
    html.P("""
        This chart represents songs' similarity based on their lyrics. 
        Each dot is a song and the closer they are in the graph, 
        the more similar the lyrics are. 
    """),
    html.P("""
        Similarity is measured by converting the words in the lyrics to number representation with embeddings and PCA,
        for nerds go see this page (put a link here)
    """),
    html.P("""
        For instance, Bohemian Rhapsody is more similar to Imagine than Child in Time. 
        Child in Time is far from the center, 
        which indicates low degree of similarity with the rest of the songs in 1999. 
    """),
    html.H5("Try it yourself!", className="text-info"),
    html.P("""
        What happened over the ranking years? Are there more outlier songs or mainstream ones? 
        Do you see the same trend for Dutch songs? How about other genres?
    """)
])