import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from data import selected_songs,feature_list


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-graph',
                    ),
                ]),width=4),

            ],            
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    # html.Label('Audio features per song'),
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': key, 'value': key} for key in feature_list],
                        value= 'Danceability'
                    ),
                ]), width=4),
                
            ],
            justify="center",
        ),
        
    ],


    # html.Div(children=[
    #     html.H4(children='Group 3 Top 2000: HW4', style={'text-align':'center'}),

    #     html.Div(children=[
    #         html.Hr(style={'border-top': '7px dotted black','width':'65%'})]),

    # ], className="row"),

    # html.Div(children=[

        

    # ])
)