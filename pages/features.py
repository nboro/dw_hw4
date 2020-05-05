import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

from dash.dependencies import Output, Input

from utils import generate_table,create_initial_era_df,create_era_df
from app import app

# DATA LOADING

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
bill_join_df = bill_join_df.dropna(subset=['main_genre','is_dutch'])

genres = bill_join_df['main_genre'].unique().tolist()

bill_join_df.is_dutch = bill_join_df.is_dutch.map({True:'Dutch', False:'Non-Dutch'})
origin_list = bill_join_df.is_dutch.unique().tolist()

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence','Tempo']

feature_desc = {
    'Valence':'Musical positiveness (e.g. happy, cheerful, euphoric) conveyed by a track.'
    ,'Liveness':'The presence of an audience in the recording.'
    ,'Instrumentalness':'Whether a track contains no vocals.' 
    ,'Speachiness':'The presence of spoken words in a track.'
    ,'Energy':'	Perceptual measure of intensity and activity.'
    ,'Danceability':'How suitable a track is for dancing.'       
    ,'Tempo':'The overall estimated tempo of a track in beats per minute (BPM).'
    ,'Loudness':'The overall loudness of a track in decibels (dB).',
}

features_descriptions = pd.DataFrame.from_dict(feature_desc,orient='index')
features_descriptions = features_descriptions.reset_index()
features_descriptions = features_descriptions.rename(columns={0:'Feature description','index':'Features'})

color_sequence=["#bdbdbd", "#9ecae1", "#3182bd"]

# CONTENT
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.H3("Comparing Features of Different Song Eras (based on Spotify API)")
                ]),className="text-center",),
            ]
        ),
        dbc.Row(
            [
                # dbc.Col(html.Div([
                #     html.P("Filters")
                # ]),width={"size":1,"order":1,"offset": 1}),
                dbc.Col(html.Div([
                    dcc.Dropdown(
                        id='genres',
                        options=[{'label': key, 'value': key} for key in genres],
                        value= 'rock'
                    ),
                ]),width={"size":3,"order":1,"offset": 2}),
                dbc.Col(html.Div([
                    dcc.Dropdown(
                        id='dutch',
                        options=[{'label': key, 'value': key} for key in origin_list],
                        value= 'Dutch'
                    ),
                ]),width={"size":3,"order":2,"offset": 12}),
            ],
        style={'margin-top':'20px'}),
        dbc.Row(
            [
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-99',
                        config=dict(responsive=True),
                        # figure = fig
                    ),
                ]),width="auto"),
                dbc.Col(generate_table(features_descriptions, max_rows=8),width="auto",align="center"),
            ],            
            justify="center",
        ),
        html.Div(id='app-1-display-value'),
        # dcc.Link('Go to App 2', href='/apps/app2')       
    ],
)


#CALLBACKS

#genre dropdown
@app.callback(
    Output('song-feature-99', 'figure'),
    [
        Input('genres', 'value'),
        Input('dutch', 'value')
    ])
def update_figure_genre(selected_genre, selected_origin,):
    
    filtered_genre = bill_join_df[bill_join_df['main_genre'] == selected_genre]
    filtered_genre = filtered_genre[filtered_genre['is_dutch'] == selected_origin]

    create_initial_era_df(filtered_genre)
    best_era_df = create_era_df(filtered_genre)

    traces = []
    for i in best_era_df['Song Era'].unique():
        df = best_era_df[best_era_df['Song Era'] == i]
        traces.append(dict(
            x=df['Compared to Oldies (Song Released < 1990)'],
            y=df['Song Features'],
            # text= df["title"],
            mode='markers',
            # color=,
            opacity=0.7,
            marker=dict(
                line_width=1, 
                symbol='circle', 
                size=16,
                color= color_sequence[np.where(best_era_df['Song Era'].unique() == i)[0][0]]
            ),
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            # title = 'Comparing Features of Different Song Eras (based on Spotify API)',
            xaxis=dict(
                title = '',
                showgrid=False,
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                dtick=25,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)',
                ticksuffix='%'
            ),
            yaxis=dict(title='Song features'),
            margin=dict(l=140, r=0, b=50, t=80),
            legend=dict(
                font_size=10,
                yanchor='middle',
                xanchor='right',
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='closest',
            width=1024,
            height=760,
        )
    }

