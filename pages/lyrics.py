import math
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

with open(f"data/lyric.json", "r") as f:
    all_df = pd.DataFrame.from_dict(json.load(f), orient="index")


def get_figure(lang, genres, bill_year, search_input, search_dropdown):
    temp_lang = lang if lang else "en"
    lyric_df = all_df[(all_df["bill_year"] == bill_year) & all_df.index.str.contains(lang)].copy()
    grouped_genre = lyric_df["main_genre"].apply(
        lambda genre: genre if genre in ["rock", "pop"] else "other"
    )
    lyric_df = lyric_df[grouped_genre.isin(genres)]
    if len(search_input) > 0:
        mask = lyric_df[search_dropdown].str.contains(search_input) if search_dropdown and search_dropdown != "all" \
            else lyric_df["artists"].str.contains(search_input) | lyric_df["title"].str.contains(search_input)
    else:
        mask = True
    colors = ["#8da0cb", "#66c2a5", "#fc8d62"]
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
                    "size": 10,
                    "opacity": 0.8 if m else 0.1,
                    "color": colors[i] if m else "#666666",
                    # "line": {
                    #     "width": 1,
                    #     "color": "DarkSlateGrey"
                    # }
                },
            }
            if m:
                trace["hovertemplate"] = "<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Rank=%{customdata[2]}"
            else:
                trace["hoverinfo"] = "skip"
            traces.append(trace)

    figure = {
        "data": traces,
        "layout": {
            "hovermode": "closest",
            "xaxis": {
                # "showgrid": False,
                "zeroline": False,
                # "showticklabels": False
            },
            "yaxis": {
                # "showgrid": False,
                "zeroline": False,
                # "showticklabels": False
            },
            "legend": {
                "x": 0.5,
                "y": -0.2,
                "xanchor": "center",
                "yanchor": "top",
                "orientation": "h"
            }
        }
    }
    return figure


def get_artist_table(title, artists, first_artist_img, genre, song_year, debut_year, hp, hp_years, similar_songs):
    table_components = [
        html.Tr([html.Th(title, colSpan=2, style={"text-align": "center"})]),
        html.Tr([html.Td(f"by {artists}", colSpan=2, style={"text-align": "center"})]),
        html.Tr([html.Td(html.Img(src=first_artist_img, height=120), colSpan=2, style={"text-align": "center"})]),
        html.Tr([html.Td("Released", style={"text-align": "right"}), html.Td(song_year)]),
        html.Tr([html.Td("Genre", style={"text-align": "right"}), html.Td(genre)]),
        html.Tr([html.Td("First Year in Chart", style={"text-align": "right"}), html.Td(debut_year)]),
        html.Tr([html.Td("Highest Position", style={"text-align": "right"}), html.Td(f"{hp} {hp_years}")]),
        html.Tr([html.Th("The lyric is similar to...", colSpan=2, style={"text-align": "center"})])
    ]
    for similar_song in similar_songs:
        table_components += [
            html.Tr([
                html.Td(html.Img(src=similar_song[0], height=80), style={"text-align": "right"}, rowSpan=2),
                html.Td(f"{similar_song[1]} ({similar_song[2]}%)")
            ]),
            html.Tr([
                html.Td(f"by {similar_song[3]}")
            ])
        ]
    return dbc.Table(table_components)


body_container = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Language"),
                dcc.Dropdown(
                    id="language-dropdown",
                    options=[{"label": "English", "value": "en"}, {"label": "Dutch", "value": "nl"}],
                    value="en"
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Genre"),
                dcc.Checklist(
                    id="genre-checklist",
                    options=[
                        {"label": "Rock", "value": "rock"},
                        {"label": "Pop", "value": "pop"},
                        {"label": "Other", "value": "other"},
                    ],
                    value=["rock", "pop", "other"],
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Search"),
                dcc.Dropdown(
                    id="search-dropdown",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Artists", "value": "artists"},
                        {"label": "Titles", "value": "title"},
                    ],
                    value="all"
                ),
                dcc.Input(
                    id="search-input",
                    value="",
                    type="text"
                )
            ])
        ], width=4)
    ]),
    dcc.Graph(
        id="fig",
        figure=get_figure("en", ["rock", "pop", "other"], 1999, "", "all")
    ),
    dcc.Slider(
        id='ranking-year-slider',
        min=1999,
        max=2019,
        value=1999,
        marks={str(year): str(year) for year in range(1999, 2020)},
        step=None
    )
]


description = html.Div(id="detail", children="Description")


content = dbc.Container([
    dbc.Row([
        dbc.Col(body_container, width=8),
        dbc.Col([
            dbc.Row(children=description)
        ], width=4)
    ])
], fluid=True)


@app.callback(
    Output("fig", "figure"),
    [
        Input("language-dropdown", "value"),
        Input("genre-checklist", "value"),
        Input("ranking-year-slider", "value"),
        Input("search-input", "value"),
        Input("search-dropdown", "value")
    ]
)
def display_figure(lang, genres, ranking_year, search_input, search_dropdown):
    return get_figure(lang, genres, ranking_year, search_input, search_dropdown)


@app.callback(
    Output("detail", "children"),
    [
        Input("language-dropdown", "value"),
        Input("fig", "clickData")
    ]
)
def display_artist_info(lang, click_data):
    temp_lang = lang if lang else "en"
    if click_data is None or "text" not in click_data["points"][0]:
        return [html.Div("Click an artist")]
    with open("data/artist_images.json", "r") as f_in:
        img_dict = json.load(f_in)
    curr_song_id = click_data["points"][0]["text"]
    song_data = all_df[all_df["song_id"] == curr_song_id].iloc[0]
    artists = song_data["artists"]
    title = song_data["title"]
    genre = song_data["main_genre"]
    hp = song_data["hp"]
    song_year = song_data["year"]
    debut_year = song_data["debut_year"]
    hp_years = song_data["hp_years"]
    first_artist = song_data["first_artist"]
    first_artist_img = img_dict[first_artist]["images"][1]["url"] if first_artist in img_dict else None
    similar_songs = []
    for sim in song_data["similar"]:
        sim_title = sim["title"]
        sim_artists = sim["all_artists"]
        sim_prob = "%.2f" % (sim["similarity"] * 100)
        sim_first_artist = sim["first_artist"]
        sim_first_artist_img = img_dict[sim_first_artist]["images"][1]["url"] if sim_first_artist in img_dict else None
        similar_songs.append((
            sim_first_artist_img,
            sim_title,
            sim_prob,
            sim_artists
        ))
    return get_artist_table(title, artists, first_artist_img, genre, song_year, debut_year, hp, hp_years, similar_songs)
