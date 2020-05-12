import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

from dash.dependencies import Output, Input

from utils import create_initial_era_df,create_era_df,get_graph_template
from app import app

graph_settings = get_graph_template()
graph_settings["layout"]["xaxis"]["showgrid"] = False
graph_settings["layout"]["xaxis"]["dtick"] = 25
graph_settings["layout"]["xaxis"]["ticksuffix"] = "%"
graph_settings["layout"]["xaxis"]["fixedrange"] = True
graph_settings["layout"]["xaxis"]["range"] = [-105, 100]
graph_settings["layout"]["yaxis"]["title"] = "Song Features"
graph_settings["layout"]["yaxis"]["fixedrange"] = True
graph_settings["layout"]["margin"]["pad"] = 20
graph_settings["layout"]["yaxis"]["zeroline"] = False
# graph_settings["layout"]["clickmode"] = 'event'
graph_settings["layout"]["legend"] = {
    "font_size": 10,
    "yanchor": "middle",
    "xanchor": "right"
}

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
bill_join_df.is_dutch = bill_join_df.is_dutch.map({True:'Dutch', False:'International'})
origin_list = bill_join_df.is_dutch.unique().tolist()
origin_list.append('All')

color_sequence = ["#f0ad4e", "#5bc0de", "#d9534f"]

content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Country:"),
                dbc.Select(
                    id='dutch',
                    options=[{'label': key, 'value': key} for key in origin_list],
                    value='All',
                    disabled=True
                )
            ])
        ], width=4),
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Genre:"),
                dbc.Select(
                    id="genres",
                    options=[{'label': 'All', 'value': 'All'}],
                    value='All',disabled=True
                )
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='song-feature-intro',
                figure={"data": [], "layout": graph_settings["layout"]},
                config=graph_settings["config"]
            ),
        ])
    ]),
]

title = "Comparing Song Features of Different Eras"

description = html.Div(children=[
    html.H5("Identifying song characteristics among eras", className="text-info"),
    html.P("""
        For each song in our dataset we retrieved quantitative measures for 9 song features from Spotify API. 
    """),
    html.P("""
        We split the dataset into 3 eras and then computed the mean value for each feature for every era. The value represents the relative difference to the oldest era (1920-1989)".
    """),
    dcc.Markdown("""
        As an example, on the left side we can see that the **Instrumentalness** of the 90s is 61.8% lower and the 2000s is 74.0% lower than the oldies. So, the old songs tend to be more instrumental than the more recent songs.
    """),
    # html.P("""
    #     For instance, Bohemian Rhapsody is more similar to Imagine than Child in Time. 
    #     Child in Time is far from the center, 
    #     which indicates low degree of similarity with the rest of the songs in 1999. 
    # """,className="text-justify"),
    html.H5("Try it yourself!", className="text-info"),
    html.P("""
        Does the song feature information provide eventually insights regarding our hypothesis? Do these insights align for dutch songs and international songs? Can we combine information from two or more features?
    """)
])

@app.callback(
    Output('song-feature-intro', 'figure'),
    [
        Input('genres', 'value'),
        Input('dutch', 'value')
    ])
def update_figure_genre(selected_genre, selected_origin):  

    create_initial_era_df(bill_join_df)
    best_era_df = create_era_df(bill_join_df)

    best_era_df = best_era_df[best_era_df['Song Features'] == 'Instrumentalness']

    best_era_df = best_era_df.reset_index(drop=True)
    best_era_df['Compared to Oldies (Song Released < 1990)'] = round(best_era_df['Compared to Oldies (Song Released < 1990)'],1)

    traces = []
    
    for i in best_era_df['Song Era'].unique():
        df = best_era_df[best_era_df['Song Era'] == i]
        
        diff = ''
        diff2 = 'markers+text'
        if i == '1920-1989':
            diff = 'The oldest era'
            # diff2= 'markers'
        else:    
            text = str(round(df.iloc[0]['Compared to Oldies (Song Released < 1990)'],1))
            diff = 'The difference<br>from the<br>oldest era<br>is '+text+'%'
            # diff2= 'markers+text'

        text_posistion = ''
        if i == '1990-1999':
            text_posistion = 'top right'
        elif i == '2000-2020':
            text_posistion = 'bottom left'
        else:
            text_posistion = 'top right'
        
        traces.append(dict(
            x=df['Compared to Oldies (Song Released < 1990)'],
            y=df['Song Features'],
            text= diff,
            mode=diff2,
            hoverinfo='skip',
            textposition = text_posistion,
            opacity=0.7,
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