import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

from dash.dependencies import Output, Input

from utils import generate_table
from app import app

# DATA LOADING

with open('data/best_era_df.pkl', 'rb') as input_file:
    best_era_df = pickle.load(input_file)

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence','Tempo']

feature_desc = {
    'Danceability':'How suitable a track is for dancing.'
    ,'Energy':'	Perceptual measure of intensity and activity.'
    ,'Speachiness':'The presence of spoken words in a track.'
    ,'Instrumentalness':'Whether a track contains no vocals.'
    ,'Liveness':'The presence of an audience in the recording.'
    ,'Valence':'Musical positiveness (e.g. happy, cheerful, euphoric) conveyed by a track.'
    ,'Tempo':'The overall estimated tempo of a track in beats per minute (BPM).'
}

features_descriptions = pd.DataFrame.from_dict(feature_desc,orient='index')
features_descriptions = features_descriptions.reset_index()
features_descriptions = features_descriptions.rename(columns={0:'Feature description','index':'Features'})

color_sequence=["#bdbdbd", "#9ecae1", "#3182bd"]

fig_dict = {
    'data':[
        dict(
            x=best_era_df[best_era_df['Song Era'] == i]['Compared to Oldies (Song Released < 1990)'],
            y=best_era_df[best_era_df['Song Era'] == i]['Song Features'],
            mode='markers',
            marker=dict(
                line_width=1, 
                symbol='circle', 
                size=16,
                color= color_sequence[np.where(best_era_df['Song Era'].unique() == i)[0][0]]
            ),
            name = i
        ) for i in best_era_df['Song Era'].unique()
    ],
    # 'template':'plotly_white',
    'layout':dict(
        title='Comparing Features of Different Song Eras (based on Spotify API)',                                xaxis=dict(
            title='Compared to Oldies (Song Released < 1990)',
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
    )
}
fig = go.Figure(fig_dict)
# CONTENT

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H2('Data Visualization - Top 2000 Group 3'),className="text-center",
                style={'text-decoration':'underline'}),
            ]
        ),
        dbc.Row(
            [
                # dbc.Col(html.Div([
                #     dcc.Dropdown(
                #         id='oldest-first',
                #         options=[{'label': key, 'value': key} for key in feature_list],
                #         value= 'Danceability'
                #     ),
                # ]),width=2,align="center"),
                dbc.Col(html.Div(children=[
                    dcc.Graph(
                        id='song-feature-99',
                        config=dict(responsive=True),
                        figure = fig
                    ),
                ]),width=8),
            ],            
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(generate_table(features_descriptions, max_rows=7),width=8),
            ],justify="center",
        ),
        html.Div(id='app-1-display-value'),
        # dcc.Link('Go to App 2', href='/apps/app2')       
    ],
)


# CALLBACKS
