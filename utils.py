import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pickle
import json

song_features = [
    'duration_ms', 'analysis_loudness', 'analysis_tempo',
    'feature_danceability', 'feature_energy', 'feature_speechiness', 'feature_instrumentalness', 
    'feature_liveness', 'feature_valence'
]

feature_desc = {
    'Valence':'Musical positiveness (e.g. happy, cheerful, euphoric) conveyed by a track.'
    ,'Liveness':'The presence of an audience in the recording.'
    ,'Instrumentalness':'Whether a track contains no vocals.' 
    ,'Speechiness':'The presence of spoken words in a track.'
    ,'Energy':'	Perceptual measure of intensity and activity.'
    ,'Danceability':'How suitable a track is for dancing.'       
    ,'Tempo':'The overall estimated tempo of a track in beats per minute (BPM).'
    ,'Loudness':'The overall loudness of a track in decibels (dB).'
    # ,'Mainstream': 'The number of followers of the artis on spotify'
    ,'Duration':'The duration of the song'
}

def get_graph_template():
    return {
        "layout": {
            "hovermode": "closest",
            "paper_bgcolor": "#2B3E50",
            "plot_bgcolor": "#2B3E50",
            "xaxis": {
                "color": "#EBEBEB",
                "automargin": True
            },
            "yaxis": {
                "color": "#EBEBEB",
                "automargin": True
            },
            "font": {
                "family": "Roboto",
                "size": 14,
                "color": "#EBEBEB"
            },
            "colorway": ["#f0ad4e", "#5bc0de", "#d9534f"],
            "hoverlabel": {
                "font": {
                    "family": "Roboto"
                }
            },
            "margin": {
                "r": 2,
                "t": 2
            }
        },
        "config": {
            "displayModeBar": False
        }
    }


def get_nav_buttons(prev_icon, prev_url, next_icon, next_url):
    buttons = []
    if prev_icon:
        buttons.append(
            dcc.Link(
                dbc.Button(
                    html.Span(
                        className=f"oi {prev_icon}",
                        title="Prev"
                    ),
                    outline=True,
                    color="light",
                    size="sm"
                ),
                id="prev-page",
                href=prev_url
            )
        )
    if next_icon:
        buttons.append(
            dcc.Link(
                dbc.Button(
                    html.Span(
                        className=f"oi {next_icon}",
                        title="Next"
                    ),
                    outline=True,
                    color="primary",
                    size="sm"
                ),
                id="next-page",
                href=next_url
            )
        )
    return dbc.ButtonGroup(buttons) if len(buttons) > 0 else ""


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


def get_lyric_snippet(song_data):
    lyric_row = []
    lyric_snippet = [snippet for snippet in song_data["lyric_snippet"][:100].split("|") if snippet]
    for i, lyric in enumerate(lyric_snippet):
        if i < len( lyric_snippet ) - 1:
            lyric_row += [html.Small(html.Em(lyric)), html.Br()]
        else:
            lyric_row.append(html.Small(html.Em(lyric + "...")))
    return lyric_row


def get_song_card(song_id, similars=None):
    with open("data/song_card.json", "r") as f_in:
        songs = json.load(f_in)
    song_data = songs[song_id]
    artists = song_data["artists"]
    title = song_data["title"]
    genre = song_data["main_genre"]
    hp = song_data["hp"]
    hp_idx = song_data["bill_ranks"].index(hp)
    song_year = song_data["year"]
    first_artist_img = song_data["first_artist_img"]
    valid_idx = [i for i, r in enumerate(song_data["bill_ranks"]) if r <= 200]
    card_contents = [
        dbc.CardHeader([
            html.H4(html.Strong(title, className="card-title text-info")),
            html.H6(artists, className="card-subtitle text-muted")
        ]),
        dbc.CardBody([
            html.Img(src=first_artist_img, height=125, alt="Artist Image",
                     className="card-text border mx-auto d-block"
                     )
        ])
    ]
    if similars:
        lyric_row = get_lyric_snippet(song_data)
        similar_rows = [
            html.P(lyric_row, className="text-center"),
            dbc.Label("The lyric is similar to:")
        ]
        for i, similar in enumerate(similars):
            similar_song_id = similar["song_id"]
            similar_song_data = songs[similar_song_id]
            similar_lyric_row = get_lyric_snippet(similar_song_data)
            similar_rows += [
                dbc.Progress(
                    html.Small("%.1f" % (similar["similarity"] * 100) + "%"),
                    value=similar["similarity"] * 100,
                    className="",
                    style={"height": "10px"}
                ),
                html.P([
                    html.Span(similar["title"] + " ", className="text-info"),
                    html.Small(
                        html.Span(className="oi oi-musical-note text-primary"),
                        id=f"similar-lyric-{i}"
                    ),
                    dbc.Tooltip(
                        similar_lyric_row,
                        target=f"similar-lyric-{i}",
                        placement="right"
                    ),
                    html.Br(),
                    html.Small(similar["all_artists"], className="text-muted")
                ])
            ]
        card_contents.append(dbc.CardBody(similar_rows))
    else:
        card_contents += [
            dbc.CardBody([
                html.Table([
                    html.Tr([html.Td(html.Strong("Released in", className="text-info")), html.Td(song_year)]),
                    html.Tr([html.Td(html.Strong("Genre", className="text-info")), html.Td(genre)])
                ], className="card-table")
            ]),
            dbc.CardBody([
                dbc.Label("Positions:"),
                dcc.Graph(
                    figure={
                        "data": [{
                            "x": [song_data["bill_years"][i] if i in valid_idx else None for i in
                                  range(len( song_data["bill_years"]))],
                            "y": [song_data["bill_ranks"][i] if i in valid_idx else None for i in
                                  range(len(song_data["bill_ranks"]))],
                            "hoverinfo": "skip",
                            "mode": "line",
                            "line": {
                                "color": "#5bc0de",
                                "width": 1
                            }
                        }, {
                            "name": "",
                            "x": [song_data["bill_years"][i] if i != hp_idx else None for i in valid_idx],
                            "y": [song_data["bill_ranks"][i] if i != hp_idx else None for i in valid_idx],
                            "customdata": [
                                (song_data["bill_ranks"][i], song_data["bill_years"][i]) if i != hp_idx else None for i in
                                valid_idx
                            ],
                            "hovertemplate": "%{customdata[0]} (%{customdata[1]})",
                            "mode": "markers",
                            "marker": {
                                "color": "#5bc0de"
                            }
                        }, {
                            "name": "",
                            "x": [song_data["bill_years"][hp_idx]],
                            "y": [song_data["bill_ranks"][hp_idx]],
                            "text": [song_data["bill_ranks"][hp_idx]],
                            "customdata": [(song_data["bill_ranks"][hp_idx], song_data["bill_years"][hp_idx])],
                            "hovertemplate": "%{customdata[0]} (%{customdata[1]})",
                            "mode": "markers+text",
                            "textposition": "top-center",
                            "marker": {
                                "color": "#DF691A"
                            }
                        }],
                        "layout": {
                            "hovermode": "closest",
                            "plot_bgcolor": "#4E5D6C",
                            "paper_bgcolor": "#4E5D6C",
                            "showlegend": False,
                            "xaxis": {
                                "range": [1998, 2020],
                                "color": "#EBEBEB",
                                "showgrid": False,
                                "automargin": True,
                                "tickmode": "array",
                                "tickvals": [2000, 2010, 2020],
                                "ticktext": ["'00", "'10", "'20"]
                            },
                            "yaxis": {
                                "range": [205, -30],
                                "color": "#EBEBEB",
                                "automargin": True,
                                "zeroline": False,
                                "tickmode": "array",
                                "tickprefix": "Top-",
                                "tickvals": [10, 50, 100, 200]
                            },
                            "font": {
                                "family": "Roboto",
                                "size": 12,
                                "color": "#EBEBEB"
                            },
                            "margin": {
                                "l": 2,
                                "r": 2,
                                "t": 2,
                                "b": 2
                            },
                            "width": 240,
                            "height": 180
                        }
                    },
                    config={
                        "displayModeBar": False
                    }
                )
            ])
        ]

    return dbc.Card(card_contents, style={"width": "18rem"})

def get_song_card_feature(song_id, feature,feature_desc,era,song_id2,era2,similars=None):
    with open("data/song_card.json", "r") as f_in:
        songs = json.load(f_in)
    song_data = songs[song_id]
    artists = song_data["artists"]
    title = song_data["title"]
    genre = song_data["main_genre"]
    # hp = song_data["hp"]

    song_data2 = songs[song_id2]
    artist2 = song_data2["artists"]
    title2 = song_data2["title"]

    first_artist_img = song_data["first_artist_img"]
    second_artist_img = song_data2["first_artist_img"]

    table_text = dcc.Markdown('''The song with the highest *'''+feature+'''* in the era **'''+ era+ '''** ''' +''' is:''')
    # table_text = dbc.Table(table_text_body,bordered=False)
    message_text =''

    card_contents = [
        dbc.CardHeader([
            html.H4(html.Strong(feature, className="card-title text-info")),
            html.H6(feature_desc, className="card-subtitle")
        ]),
        dbc.CardBody([
            html.Table([html.Tr([html.Td(table_text)])], className="card-table"),
            html.Img(src=first_artist_img, height=125, alt="Artist Image",
                className="card-text border mx-auto d-block",style={'margin-bottom':'15px'}),
            html.Table([
                html.Tr([html.Td(html.Strong("Song Title", className="text-info")), html.Td(title)]),
                html.Tr([html.Td(html.Strong("Performed by", className="text-info")), html.Td(artists)]),
                html.Tr([html.Td(html.Strong("Genre", className="text-info")), html.Td(genre)]),
            ], className="card-table")
        ])
    ]
    if song_id == song_id2:
        message_text = dcc.Markdown('''This is also the song with the highest *'''+feature+'''* among **ALL eras**.''')
        card_contents += [
            dbc.CardBody([
                html.Table([html.Tr([html.Td(message_text)])], className="card-table"),
            ]),
        ]
    else:
        message_text = dcc.Markdown('''The song with the highest *'''+feature+'''* among **ALL eras** is:''')
        card_contents += [
            dbc.CardBody([
                html.Table([html.Tr([html.Td(message_text)])], className="card-table"),
                html.Img(src=second_artist_img, height=125, alt="Artist Image",
                     className="card-text border mx-auto d-block",style={'margin-bottom':'15px'}
                     ),
                html.Table([
                    html.Tr([html.Td(html.Strong("Song Title", className="text-info")), html.Td(title2)]),
                    html.Tr([html.Td(html.Strong("Performed by", className="text-info")), html.Td(artist2)]),
                    html.Tr([html.Td(html.Strong("Era", className="text-info")), html.Td(era2)]),
                    html.Tr([html.Td(html.Strong("Genre", className="text-info")), html.Td(genre)]),
                ], className="card-table")
            ]),
        ]

    return dbc.Card(card_contents, style={"width": "18rem"})


def create_initial_era_df(df):

    era_df = df.groupby(["title", "era", "hp"]).count().reset_index()[["title", "era", "hp", "artist"]].rename(columns={"artist": "count"})
    era_df["era_rank"] = era_df.groupby("era")["hp"].rank(method="first")
    best_era_df = df[df["title"].isin(era_df[era_df["era_rank"] < 200]["title"].unique())].copy()[["title", "era"] + song_features].dropna().reset_index()
    first_title_df = best_era_df[["index", "title"]].groupby("title")["index"].rank(method="first")
    best_era_df = best_era_df[first_title_df == 1]
    del best_era_df["index"]
    del best_era_df["title"]
    best_era_df.columns = [
        "era", "Duration", "Loudness", "Tempo",
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

def get_max_each_feature(df,era,genre,origin):

    max_songs={}
    max_songs_general={}
    
    if origin != 'All':
        df_filtered = df[df['is_dutch'] == origin]
    else:
        df_filtered = df

    df_filtered = df_filtered[df_filtered['main_genre'] == genre]

    df_filtered2 = df_filtered[df_filtered['era'] == era]

    for feature in song_features:
        # print(feature)
        row = df_filtered2.loc[df_filtered2[feature].idxmax()]        
        max_songs[feature] = row['song_id']

        row_general = df_filtered.loc[df_filtered[feature].idxmax()]
        max_songs_general[feature] = row_general['era']+'_'+row_general['song_id']
    
    return max_songs,max_songs_general