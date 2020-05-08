import math
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import get_graph_template, get_song_card
from copy import deepcopy

from app import app

# LOAD DATA
with open(f"data/lyric.json", "r") as f:
    all_df = pd.DataFrame.from_dict(json.load(f), orient="index")


# TEMPLATE SETTINGS
graph_settings = get_graph_template()
graph_settings["layout"]["xaxis"]["zeroline"] = False
graph_settings["layout"]["xaxis"]["fixedrange"] = True
graph_settings["layout"]["xaxis"]["showgrid"] = False
graph_settings["layout"]["xaxis"]["showticklabels"] = False
graph_settings["layout"]["yaxis"]["zeroline"] = False
graph_settings["layout"]["yaxis"]["fixedrange"] = True
graph_settings["layout"]["yaxis"]["showgrid"] = False
graph_settings["layout"]["yaxis"]["showticklabels"] = False
graph_settings["layout"]["legend"] = {
    "title": {
        "text": "Song Release Year"
    },
    "x": 0,
    "y": 1,
    "xanchor": "left",
    "yanchor": "top"
}


# FUNCTIONS
def get_figure(lang, genre, bill_year, search_text, search_type):
    layout_settings = deepcopy(graph_settings["layout"])
    lyric_df = all_df[(all_df["bill_year"] == bill_year) & all_df.index.str.contains(lang)].copy()
    if genre in ("rock", "pop"):
        lyric_df = lyric_df[lyric_df["main_genre"] == genre]
    elif genre == "other":
        lyric_df = lyric_df[~lyric_df["main_genre"].isin(["rock", "pop"])]
    mask = True
    if len(search_text) > 0:
        mask = lyric_df[search_type].str.contains(search_text, case=False) \
            if search_type != "both" else \
            lyric_df["artists"].str.contains(search_text, case=False) | \
            lyric_df["title"].str.contains(search_text, case=False)

    layout_settings["yaxis"]["range"] = [-0.35, 0.65] if lang == "en" else [-0.15, 0.2]
    layout_settings["xaxis"]["range"] = [-0.5, 0.7] if lang == "en" else [-0.2, 0.2]

    if len(lyric_df) == 0:
        layout_settings["annotations"] = [{
            "name": "empty set",
            "text": "Oops, nothing to see here. Try another filter.",
            "opacity": 0.5,
            "x": 0,
            "y": 0,
            "xanchor": "center",
            "yanchor": "center",
            "showarrow": False
        }]
        figure = {
            "data": [],
            "layout": layout_settings
        }
        return dcc.Graph(id="lyric-fig", figure=figure, config=graph_settings["config"])

    traces = []
    names = {
        "oldies": "1920-1989",
        "90s": "1990-1999",
        "2000s": "2000-2019"
    }
    for m in [False, True]:
        for i, state in enumerate(["oldies", "90s", "2000s"]):
            trace_df = lyric_df[(lyric_df["era"] == state) & mask] if m else lyric_df[(lyric_df["era"] == state) & ~mask]
            custom_data = [(r["title"], r["artists"], r["bill_rank"], idx) for idx, r in trace_df.iterrows()]
            trace = {
                "name": names[state],
                "x": trace_df["pca1"],
                "y": trace_df["pca2"],
                "mode": "markers",
                "text": trace_df["song_id"],
                "customdata": custom_data,
                "showlegend": m,
                "marker": {
                    "symbol": "circle",
                    "size": 11,
                    "opacity": 0.8 if m else 0.1,
                    "line": {
                        "width": 0.5,
                        "color": "#2B3E50"
                    }
                },
            }
            if m:
                trace["hovertemplate"] = "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Rank=%{customdata[2]}"
            else:
                trace["hoverinfo"] = "skip"
            traces.append(trace)

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
                        {"label": "Other", "value": "other"},
                    ],
                    value="all"
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
                    type="text"
                ),
                dbc.RadioItems(
                    id="search-radio",
                    options=[
                        {"label": "Both", "value": "both"},
                        {"label": "Artist", "value": "artists"},
                        {"label": "Titles", "value": "title"},
                    ],
                    value="both",
                    inline=True
                ),
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col(
            get_figure("en", "all", 1999, "", "both"),
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
                className="custom-range"
            )
        ]),
    ])
]


title = "The Lyric Constellation"

description = html.Div(id="lyric-description", children="Click an artist")


# CALLBACKS
@app.callback(
    Output("lyric-fig-col", "children"),
    [
        Input("language-dropdown", "value"),
        Input("genre-dropdown", "value"),
        Input("ranking-year-slider", "value"),
        Input("search-input", "value"),
        Input("search-radio", "value")
    ]
)
def display_figure(lang, genres, ranking_year, search_input, search_radio):
    return get_figure(lang, genres, ranking_year, search_input, search_radio)


@app.callback(Output("lyric-description", "children"), [Input("lyric-fig", "clickData")])
def display_artist_info(click_data):
    if click_data is None or "text" not in click_data["points"][0]:
        return [html.Div("Click an artist")]
    curr_song_id = click_data["points"][0]["text"]
    curr_df_id = click_data["points"][0]["customdata"][3]
    similars = all_df.loc[curr_df_id]["similar"]
    return get_song_card(curr_song_id, similars)
