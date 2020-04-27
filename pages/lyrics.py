import math
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

artist_df = pd.read_json("data/artist_graph.json", orient="index")


def get_figure(lang, size, color):
    all_df = artist_df[artist_df["lang"] == lang]

    colors = ["#fc8d62", "#8da0cb", "#66c2a5"]
    traces = []
    edge_x = []
    edge_y = []
    for _, row in all_df.iterrows():
        x0, y0 = row["pos"]
        x1, y1 = row["pos_sim_1"]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    traces.append({
        "name": "Most Similar With",
        "x": edge_x,
        "y": edge_y,
        "mode": "lines",
        "hoverinfo": "none",
        "line": {
            "width": 0.5,
            "color": "DarkSlateGrey",
            "shape": "spline"
        }
    })
    if color == "era":
        color_cats = ["oldies", "90s", "2000s"]
        labels = ["Before 1990", "1990-2000", "After 2000"]
    else:
        color_cats = ["rock", "pop", "other"]
        labels = ["Rock", "Pop", "Other Genres"]
    for i, c in enumerate(color_cats):
        artist_graph_df = all_df[all_df[color] == c] if c != "other" else all_df[~all_df[color].isin(color_cats[:-1])]
        node_x = [pos[0] for pos in artist_graph_df["pos"]]
        node_y = [pos[1] for pos in artist_graph_df["pos"]]
        hover_remark = {
            "node_adjacencies": "connection",
            "song_count": "song"
        }
        custom_data = [[
            r["artist"],
            r[size],
            hover_remark[size] + ("s" if r[size] > 1 else "")
        ] for _, r in artist_graph_df.iterrows()]
        node_text = artist_graph_df["artist"]
        node_size = [(s // 6 + 1) * 6 for s in artist_graph_df[size]]
        traces.append({
            "name": labels[i],
            "x": node_x,
            "y": node_y,
            "mode": "markers",
            "text": node_text,
            "customdata": custom_data,
            "hovertemplate": "<b>%{customdata[0]}</b><br>%{customdata[1]} %{customdata[2]}",
            "marker": {
                "symbol": "circle",
                "size": node_size,
                "opacity": 1,
                "color": colors[i],
                "line": {
                    "width": 1,
                    "color": "DarkSlateGrey"
                }
            }
        })
    figure = {
            "data": traces,
            "layout": {
                "hovermode": "closest",
                # "width": 800,
                "height": 600,
                "xaxis": {
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False
                },
                "yaxis": {
                    "showgrid": False,
                    "zeroline": False,
                    "showticklabels": False
                }
            }
        }
    return figure


def get_artist_table(img_src, name, avg_song_year, genre, num_songs, similar_artists):
    table_components = [
        html.Tr([html.Td(html.Img(src=img_src, height=120), colSpan=2, style={"text-align": "center"})]),
        html.Tr([html.Th(name, colSpan=2, style={"text-align": "center"})]),
        html.Tr([html.Td("Active Around", style={"text-align": "right"}), html.Td(avg_song_year)]),
        html.Tr([html.Td("Main Genre", style={"text-align": "right"}), html.Td(genre)]),
        html.Tr([html.Td("#Songs in Top-200", style={"text-align": "right"}), html.Td(num_songs)]),
        html.Tr([html.Th("Similar Artists", colSpan=2, style={"text-align": "center"})])
    ]
    for similar_artist in similar_artists:
        table_components.append(
            html.Tr([
                html.Td(html.Img(src=similar_artist[1], height=80), style={"text-align": "right"}),
                html.Td(similar_artist[0])
            ])
        )
    return html.Table(table_components)


content = html.Div([
    html.Div(children=[
        html.H1(children="The Artist Constellation"),
        html.H4(children="Based on lyrics similarity"),
        html.Div(children=[
            html.Div(children="Language:", style={"width": "30%", "display": "inline-block"}),
            html.Div(children="Size:", style={"width": "30%", "display": "inline-block"}),
            html.Div(children="Colors:", style={"width": "30%", "display": "inline-block"})
        ]),
        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(
                    id="language",
                    options=[{"label": "English", "value": "en"}, {"label": "Dutch", "value": "nl"}],
                    value="en"
                )
            ],
                style={"width": "30%", "display": "inline-block", "padding": "10px none"}
            ),
            html.Div(children=[
                dcc.Dropdown(
                    id="size",
                    options=[
                        {"label": "#Connections", "value": "node_adjacencies"},
                        {"label": "#Songs in Top-200", "value": "song_count"}
                    ],
                    value="node_adjacencies"
                )
            ],
                style={"width": "30%", "display": "inline-block", "padding": "10px none"}
            ),
            html.Div(children=[
                dcc.Dropdown(
                    id="color",
                    options=[
                        {"label": "Era", "value": "era"},
                        {"label": "Genre", "value": "main_genre"}
                    ],
                    value="era"
                )
            ],
                style={"width": "30%", "display": "inline-block", "padding": "10px none"}
            )
        ]),
        html.Div(children=[
            dcc.Graph(
                id="fig",
                figure=get_figure("en", "node_adjacencies", "era")
            )
        ]),
    ],
        style={"width": "70%", "display": "inline-block"}
    ),
    html.Div(
        id="artist_table",
        children=[],
        style={"width": "20%", "display": "inline-block", "vertical-align": "top", "padding": "10px"}
    )
])


@app.callback(
    Output("fig", "figure"),
    [Input("language", "value"), Input("size", "value"), Input("color", "value")]
)
def display_figure(lang, size, color):
    return get_figure(lang, size, color)


@app.callback(
    Output("artist_table", "children"),
    [
        Input("language", "value"),
        Input("fig", "clickData")
    ]
)
def display_artist_info(lang, click_data):
    if click_data is None or "text" not in click_data["points"][0]:
        return [html.Div("Click an artist...")]
    curr_artist = click_data["points"][0]["text"]
    attention_artist = artist_df[
        (artist_df["lang"] == lang) &
        (artist_df["artist"] == curr_artist)
        ]
    if len(attention_artist) == 0:
        return [html.Div("Click an artist...")]
    artist = attention_artist.iloc[0]
    genre = artist["main_genre"]
    num_songs = artist["song_count"]
    avg_song_year = math.ceil(artist["avg_song_year"])
    curr_img = artist["images"][1]["url"]
    similar_artists = []
    i = 1
    while len(similar_artists) < 3 and i < 6:
        similar_artist_name = artist[f"similar_artist_{i}"]
        similar_artist = artist_df[artist_df["artist"] == similar_artist_name]
        if len(similar_artist) > 0:
            similar_img = similar_artist.iloc[0]["images"][1]["url"]
            similar_artists.append((similar_artist_name, similar_img))
        i += 1
    return get_artist_table(curr_img, curr_artist, avg_song_year, genre, num_songs, similar_artists)
