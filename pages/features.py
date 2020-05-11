import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

from dash.dependencies import Output, Input

from utils import (create_initial_era_df, create_era_df, get_max_each_feature,
                   get_graph_template, get_song_card_feature, get_toast_hint)
from app import app


# SETUP LAYOUT AND CONFIG
graph_settings = get_graph_template()
graph_settings["layout"]["xaxis"]["showgrid"] = False
graph_settings["layout"]["xaxis"]["dtick"] = 25
graph_settings["layout"]["xaxis"]["ticksuffix"] = "%"
graph_settings["layout"]["xaxis"]["fixedrange"] = True
graph_settings["layout"]["xaxis"]["range"] = [-100, 100]
graph_settings["layout"]["yaxis"]["title"] = "Song Features"
graph_settings["layout"]["yaxis"]["fixedrange"] = True
graph_settings["layout"]["yaxis"]["zeroline"] = False
graph_settings["layout"]["clickmode"] = 'event'
graph_settings["layout"]["legend"] = {
    "font_size": 10,
    "yanchor": "middle",
    "xanchor": "right"
}

# DATA LOADING

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
bill_join_df = bill_join_df.dropna(subset=['main_genre','is_dutch','era'])
bill_join_df = bill_join_df.drop(columns=['followers'],axis =1)

bill_join_df['main_genre'] = bill_join_df['main_genre'].apply(lambda g: g if g in ["rock", "pop"] else "others")
# genres = bill_join_df['main_genre'].unique().tolist()
# genres.append("All")

bill_join_df.is_dutch = bill_join_df.is_dutch.map({True:'Dutch', False:'International'})
origin_list = bill_join_df.is_dutch.unique().tolist()
origin_list.append('All')

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence','Tempo']

feature_map = {
    'Duration':'duration_ms', 'Loudness':'analysis_loudness', 'Tempo':'analysis_tempo',
    'Danceability':'feature_danceability', 'Energy':'feature_energy', 'Speechiness':'feature_speechiness', 'Instrumentalness':'feature_instrumentalness','Liveness':'feature_liveness', 'Valence':'feature_valence'
}

era_map = {'1920-1989':'oldies', '1990-1999':'90s','2000-2020':'2000s'}

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

color_sequence = ["#f0ad4e", "#5bc0de", "#d9534f"]


def add_tags(tag, word):
    return "<%s>%s</%s>" % (tag, word, tag)

def get_key(text):
    k=''
    for key in era_map.keys():
        if era_map[key] == text:
            k=key
            return k


# CONTENTS
title = "Comparing Features of Different Song Eras (based on Spotify API)"

content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Country:"),
                dbc.Select(
                    id='dutch',
                    options=[{'label': key, 'value': key} for key in origin_list],
                    value='All'
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Genre:"),
                dbc.Select(
                    id="genres",
                    options=[{'label': 'rock', 'value': 'rock'}],  # TODO fix this with correct initial value list
                    value='All'
                )
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='song-feature-99',
                figure={"data": [], "layout": graph_settings["layout"]},
                config=graph_settings["config"]
            ),
        ])
    ]),
]

description = html.Div(id='feature_text', children=get_toast_hint())

#CALLBACKS

#genre dropdown
@app.callback(
    Output('genres', 'options'),
    [
        Input('dutch', 'value')
    ])
def update_genre(selected_origin):

    if selected_origin != "All":
        filtered_genre = bill_join_df[bill_join_df['is_dutch'] == selected_origin]
    else:
        filtered_genre = bill_join_df

    genre_list = list(filtered_genre.main_genre.unique())
    genre_list.append('All')

    return [{'label': i, 'value': i} for i in genre_list]

@app.callback(
    Output('genres', 'value'),
    [
        Input('genres', 'options')
    ])
def set_genre(available_options):

    return available_options[3]['value']

#song feature graph
@app.callback(
    Output('song-feature-99', 'figure'),
    [
        Input('genres', 'value'),
        Input('dutch', 'value')
    ])
def update_figure_genre(selected_genre, selected_origin):

    if selected_origin != "All":
        filtered_genre = bill_join_df[bill_join_df['is_dutch'] == selected_origin]
    else:
        filtered_genre = bill_join_df

    if selected_genre in ("rock", "pop"):
        filtered_genre = filtered_genre[filtered_genre["main_genre"] == selected_genre]
    elif selected_genre == "others":
        filtered_genre = filtered_genre[~filtered_genre["main_genre"].isin(["rock", "pop"])]

    # filtered_genre = filtered_genre[filtered_genre['main_genre'] == selected_genre]   

    create_initial_era_df(filtered_genre)
    best_era_df = create_era_df(filtered_genre)

    best_era_df = best_era_df.reset_index(drop=True)
    best_era_df['Compared to Oldies (Song Released < 1990)'] = round(best_era_df['Compared to Oldies (Song Released < 1990)'],1)

    traces = []
    
    for i in best_era_df['Song Era'].unique():
        df = best_era_df[best_era_df['Song Era'] == i]
        
        # diff = ''
        # if i == '1920-1989':
        #     diff = 'The era of the point of comparison'
        # else:    
        #     diff = 'is the difference from the oldest era'#+text+'%'

        custom_data = [(row['Song Era'],selected_genre,selected_origin,row['Compared to Oldies (Song Released < 1990)']) for idx, row in df.iterrows()] 

        traces.append(dict(
            x=df['Compared to Oldies (Song Released < 1990)'],
            y=df['Song Features'],
            # text= diff,
            mode='markers',
            # hoverinfo='text+x',
            hovertemplate = "The difference from the oldest era is <b>%{customdata[3]}%</b><br>" if i != '1920-1989' else 'The era of the point of comparison',
            opacity=0.7,
            customdata = custom_data,
            marker=dict(
                # line=dict(width=0.5, color='#2B3E50'),
                symbol='circle',
                size=16,
                color= color_sequence[np.where(best_era_df['Song Era'].unique() == i)[0][0]]
            ),
            name=i
        ))

    return {
        'data': traces,
        'layout': graph_settings["layout"]
    }

#click data
@app.callback(
    Output('feature_text','children'),
    [
        Input('song-feature-99','clickData')
    ]
)
def display_feature_text(clickData):
    if clickData is None or "y" not in clickData["points"][0]:
        return get_toast_hint()
    
    click = clickData['points'][0]
    era = click['customdata'][0]
    genre = click['customdata'][1]
    origin = click['customdata'][2]
    era_mapped = era_map[era]
    feature = click['y']
    feature_descr = feature_desc[feature]

    max_key = feature_map[feature]
    max_val,max_val_general = get_max_each_feature(bill_join_df,era_mapped,genre,origin)
    max_value = max_val[max_key]
    feature_max,song_id = max_value.split('_',1)

    max_value_general = max_val_general[max_key]
    era22,feature_max_general,genre2,song_id2 = max_value_general.split('_',3)
    
    era2 = get_key(era22)
    
    return get_song_card_feature(song_id, feature,feature_descr,era,song_id2,era2,feature_max,feature_max_general,genre2)
