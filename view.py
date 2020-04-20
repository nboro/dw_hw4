import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from data import feature_list


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H2('Data Visualization - Top 2000 Group 3'),className="text-center",
                style={'text-decoration':'underline'}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-99',
                    ),
                ]),width=6),
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-19',
                    ),
                ]),width=6),

            ],            
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    # html.Label('Audio features per song'),
                    dcc.Dropdown(
                        id='oldest-first',
                        options=[{'label': key, 'value': key} for key in feature_list],
                        value= 'Danceability'
                    ),
                ]), width=4),                
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    # html.Label('Audio features per song'),
                    dcc.Dropdown(
                        id='oldest-second',
                        options=[{'label': key, 'value': key} for key in feature_list],
                        value= 'Energy'
                    ),
                ]), width=4),
                
            ],
            justify="center",
        ),
        
    ],

)