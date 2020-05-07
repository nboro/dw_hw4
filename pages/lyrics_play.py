import math
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import get_graph_template, get_song_card

from app import app

# LOAD DATA
with open(f"data/lyric.json", "r") as f:
    all_df = pd.DataFrame.from_dict(json.load(f), orient="index")


# TEMPLATE SETTINGS
graph_settings = get_graph_template()
graph_settings["layout"]["xaxis"]["zeroline"] = False
graph_settings["layout"]["yaxis"]["zeroline"] = False
graph_settings["layout"]["legend"] = {
    "x": 0,
    "y": 1,
    "xanchor": "left",
    "yanchor": "top"
}


# FUNCTIONS
def get_figure(lang, genre, bill_year, search_text, search_type):
    temp_lang = lang if lang else "en"
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
    traces = []

    for m in [False, True]:
        for i, state in enumerate(["oldies", "90s", "2000s"]):
            trace_df = lyric_df[(lyric_df["era"] == state) & mask] if m else lyric_df[(lyric_df["era"] == state) & ~mask]
            custom_data = [(r["title"], r["artists"], r["bill_rank"]) for _, r in trace_df.iterrows()]
            trace = {
                "name": state,
                "x": trace_df["pca1"],
                "y": trace_df["pca2"],
                "mode": "markers",
                "text": trace_df["song_id"],
                "customdata": custom_data,
                "showlegend": m,
                "marker": {
                    "symbol": "circle",
                    "size": 8,
                    "opacity": 1 if m else 0.1
                },
            }
            if m:
                trace["hovertemplate"] = "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Rank=%{customdata[2]}"
            else:
                trace["hoverinfo"] = "skip"
            traces.append(trace)

    figure = {
        "data": traces,
        "layout": graph_settings["layout"]
    }
    return figure


def get_similar_songs(song_id):
    similar_songs = []
    # for sim in song_data["similar"]:
    #     sim_title = sim["title"]
    #     sim_artists = sim["all_artists"]
    #     sim_prob = "%.2f" % (sim["similarity"] * 100)
    #     sim_first_artist = sim["first_artist"]
    #     similar_songs.append((
    #         sim_title,
    #         sim_artists,
    #         sim_prob,
    #     ))


# CONTENTS
body_container = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Language"),
                dbc.Select(
                    id="language-dropdown",
                    options=[{"label": "English", "value": "en"}, {"label": "Dutch", "value": "nl"}],
                    value="en"
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Genre"),
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
                dbc.Label("Search"),
                dbc.Input(
                    id="search-input",
                    value="",
                    placeholder="Queen",
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
        dbc.Col([
            dcc.Graph(
                id="fig",
                figure=get_figure("en", ["rock", "pop", "other"], 1999, "", "all"),
                config=graph_settings["config"]
            )
        ], width=12)
    ])
]


description = html.Div(id="detail", children="Description")


content = dbc.Container([
    dbc.Row([
        dbc.Col(body_container, width=9),
        dbc.Col([
            dbc.Row(children=description)
        ], width=3)
    ])
], fluid=True)


@app.callback(Output("detail", "children"), [Input("fig", "clickData")])
def display_artist_info(click_data):
    if click_data is None or "text" not in click_data["points"][0]:
        return [html.Div("Click an artist")]
    curr_song_id = click_data["points"][0]["text"]
    return get_song_card(curr_song_id)