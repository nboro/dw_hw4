import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from data import feature_list, features_descriptions
from generate_table import generate_table


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
                dbc.Col(html.Div([
                    # html.Label('Audio features per song'),
                    dcc.Dropdown(
                        id='oldest-first',
                        options=[{'label': key, 'value': key} for key in feature_list],
                        value= 'Danceability'
                    ),
                ]),width=2,align="center"),
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-99',
                    ),
                ]),width=8),
            ],            
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(generate_table(features_descriptions),width=8),
            ],justify="center",
        ),       
    ]

)