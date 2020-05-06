import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pickle
import json

song_features = [
    'duration_ms', 'followers', 'analysis_loudness', 'analysis_tempo',
    'feature_danceability', 'feature_energy', 'feature_speechiness', 'feature_instrumentalness', 
    'feature_liveness', 'feature_valence'
]

default_graph = {
    "layout": {
        "hovermode": "closest",
        "paper_bgcolor": "#2B3E50",
        "plot_bgcolor": "#2B3E50",
        "xaxis": {
            "color": "#EBEBEB"
        },
        "yaxis": {
            "color": "#EBEBEB"
        },
        "legend": {
            "x": 0.5,
            "y": -0.2,
            "xanchor": "center",
            "yanchor": "top",
            "orientation": "h"
        },
        "font": {
            "family": "Roboto",
            "size": 14,
            "color": "#efdab9"
        },
        "colorway": ["#e2cd6d", "#649cc8", "#e86f68"],
        "hoverlabel": {
            "font": {
                "family": "Roboto"
            }
        },
        "margin": {
            "l": 2,
            "r": 2,
            "t": 2,
            "b": 2
        },
    },
    "config": {
        "displayModeBar": False
    }
}


def generate_table(dataframe, max_rows):

    """ A function which returns a responsive html table provided a dataframe """

    return html.Div(children=[
        html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ], className="table-bordered")
    ], className="table-responsive")


def get_song_card(song_id):
    with open("data/song_card.json", "r") as f_in:
        songs = json.load(f_in)
    song_data = songs[song_id]
    artists = song_data["artists"]
    title = song_data["title"]
    genre = song_data["main_genre"]
    hp = song_data["hp"]
    song_year = song_data["year"]
    first_artist_img = song_data["first_artist_img"]
    card = dbc.Card([
        dbc.CardHeader([
            html.H4(html.Strong(title, className="card-title text-info")),
            html.H6(artists, className="card-subtitle text-muted")
        ]),
        dbc.CardBody([
            html.Img(src=first_artist_img, height=100, alt="Artist Image", className="card-text rounded mx-auto d-block")
        ]),
        dbc.CardBody([
            html.Table([
                html.Tr([html.Td(html.Strong("Released in", className="text-info")), html.Td(song_year)]),
                html.Tr([html.Td(html.Strong("Genre", className="text-info")), html.Td(genre)])
            ])
        ]),
        dbc.CardBody([
            dcc.Graph(
                figure={
                    "data": [{
                        "x": song_data["bill_years"],
                        "y": song_data["bill_ranks"],
                        "text": song_data["bill_ranks"],
                        "mode": "markers+lines",
                        "marker": {
                            "color": "#5bc0de"
                        },
                        "line": {
                            "color": "#5bc0de"
                        }
                    }],
                    "layout": {
                        "hovermode": "closest",
                        "plot_bgcolor": "#4E5D6C",
                        "paper_bgcolor": "#4E5D6C",
                        "xaxis": {
                            "range": [1998, 2020],
                            "color": "#EBEBEB",
                            "showgrid": False,
                        },
                        "yaxis": {
                            "range": [2000, -100],
                            "zeroline": False,
                            "color": "#EBEBEB"
                        },
                        "margin": {
                            "l": 2,
                            "r": 2,
                            "t": 2,
                            "b": 2
                        },
                        "width": 200,
                        "height": 100
                    }
                },
                config={
                    "displayModeBar": False
                }
            )
        ])
    ], style={"width": "15rem", "border-radius": "5px"})
    return card


def create_initial_era_df(df):

    era_df = df.groupby(["title", "era", "hp"]).count().reset_index()[["title", "era", "hp", "artist"]].rename(columns={"artist": "count"})
    era_df["era_rank"] = era_df.groupby("era")["hp"].rank(method="first")
    best_era_df = df[df["title"].isin(era_df[era_df["era_rank"] < 200]["title"].unique())].copy()[["title", "era"] + song_features].dropna().reset_index()
    first_title_df = best_era_df[["index", "title"]].groupby("title")["index"].rank(method="first")
    best_era_df = best_era_df[first_title_df == 1]
    del best_era_df["index"]
    del best_era_df["title"]
    best_era_df.columns = [
        "era", "Duration", "Mainstream", "Loudness", "Tempo",
        "Danceability", "Energy", "Speechiness", "Instrumentalness",
        "Liveness", "Valence"
    ]

    best_era_df.to_pickle('data/best_era_df2.pkl')

def create_era_df(df):

        with open('data/best_era_df2.pkl', 'rb') as input_file:
            best_era_df2 = pickle.load(input_file)
        
        best_era_df2 = best_era_df2.groupby("era").mean().reset_index().melt(id_vars=["era"])
        compare_oldies_df = best_era_df2[best_era_df2["era"] == "oldies"][["variable", "value"]].rename(columns={"value": "value_oldies"})
        best_era_df2 = best_era_df2.merge(compare_oldies_df, how="left", on="variable")
        best_era_df2["relative_to_oldies"] = (best_era_df2["value"] - best_era_df2["value_oldies"]) * 100 / best_era_df2["value_oldies"]
        best_era_df2["era"] = best_era_df2["era"].map({"oldies": "1920-1989", "90s": "1990-1999", "2000s": "2000-2020"})
        best_era_df2 = best_era_df2[["era", "variable", "relative_to_oldies"]].sort_values(["era", "relative_to_oldies"])
        best_era_df2.columns = ["Song Era", "Song Features", "Compared to Oldies (Song Released < 1990)"]

        return best_era_df2

def get_max_each_feature(df):

    max_songs={}
    for feature in song_features:
        # print(feature)
        row = df.loc[df[feature].idxmax()]
        max_songs[feature] = row['title']+ '_'+row['artist']+'_'+row['main_genre']
    
    return max_songs