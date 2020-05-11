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
                    options=[{'label': 'rock', 'value': 'rock'}],  # TODO fix this with correct initial value list
                    value='All',
                    disabled=True
                )
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='song-feature-outro',
                figure={"data": [], "layout": graph_settings["layout"]},
                config=graph_settings["config"]
            ),
        ])
    ]),
]

title = "Comparing Features of Different Song Eras (based on Spotify API)"

description = html.Div(children=[
    html.H5("Do you recognize any trend..?", className="text-info"),
    dcc.Markdown('''***Valence*** appears to be significantly higher in the oldest era in almost all cases. This means older songs are more positive and probably that is why people prefer them.''',className="text-justify"),
    dcc.Markdown("""
        ***Speechiness*** follows the same pattern as valence. This means that probably lyrics in older songs are more positive. To support this we can observe that the instrumentalness is significantly lower in the more recent eras suggesting that although recent era songs contain more vocals probably they are less positive or people prefer short and simple.
    """,className="text-justify"),
    dcc.Markdown("""
        ***Energy***, ***Danceability*** and ***Tempo*** do not appear to have considerable differences suggesting that songs probably have not changed that much throughout the years and the reason for people’s preferences probably does not lie there. 
    """,className="text-justify"),
    # html.H5("Try it yourself!", className="text-info"),
    # html.P("""
    #     What happened over the ranking years? Are there more outlier songs or mainstream ones? 
    #     Do you see the same trend for Dutch songs? How about other genres?
    # """,className="text-justify)
])

@app.callback(
    Output('song-feature-outro', 'figure'),
    [
        Input('genres', 'value'),
        Input('dutch', 'value')
    ])
def update_figure_genre(selected_genre, selected_origin):  

    create_initial_era_df(bill_join_df)
    best_era_df = create_era_df(bill_join_df)

    f = ['Valence','Speechiness','Energy','Danceability','Tempo']
    best_era_df = best_era_df[best_era_df['Song Features'].isin(f)]

    best_era_df = best_era_df.reset_index(drop=True)
    best_era_df['Compared to Oldies (Song Released < 1990)'] = round(best_era_df['Compared to Oldies (Song Released < 1990)'],1)

    traces = []
    
    for i in best_era_df['Song Era'].unique():
        df = best_era_df[best_era_df['Song Era'] == i]        
        diff2 = 'markers+text'        
        traces.append(dict(
            x=df['Compared to Oldies (Song Released < 1990)'],
            y=df['Song Features'],
            # text= diff,
            mode=diff2,
            hoverinfo='skip',
            # textposition = text_posistion,
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