import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pickle

from dash.dependencies import Output, Input

from utils import generate_table
from app import app

# DATA LOADING

with open('data/songs_with_features.pkl', 'rb') as input_file:
    songs_with_features = pickle.load(input_file)

with open('data/songs_bill_melt.pkl', 'rb') as input_file:
    songs_bill_melt = pickle.load(input_file)

selected_songs19 = songs_with_features.head(15).sort_values(by='zero_nineteen',ascending=True)
selected_songs99 = songs_with_features[songs_with_features['ninety_nine'] > 0]
selected_songs99 = selected_songs99.head(15).sort_values(by='ninety_nine',ascending=True)

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence']

feature_desc = {
    'Danceability':'How suitable a track is for dancing.'
    ,'Energy':'	Perceptual measure of intensity and activity.'
    ,'Speachiness':'The presence of spoken words in a track.'
    ,'Instrumentalness':'Whether a track contains no vocals.'
    ,'Liveness':'The presence of an audience in the recording.'
    ,'Valence':'Musical positiveness (e.g. happy, cheerful, euphoric) conveyed by a track.'
}

features_descriptions = pd.DataFrame.from_dict(feature_desc,orient='index')
features_descriptions = features_descriptions.reset_index()
features_descriptions = features_descriptions.rename(columns={0:'Feature description','index':'Features'})


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
                dbc.Col(generate_table(features_descriptions, max_rows=6),width=8),
            ],justify="center",
        ),
        html.Div(id='app-1-display-value'),
        # dcc.Link('Go to App 2', href='/apps/app2')       
    ],
)


# CALLBACKS
@app.callback(
    Output('song-feature-99', 'figure'),
    [Input('oldest-first', 'value')])
def update_graph99(oldest_first_value):

    # years = list(songs_bill_melt.bill_year.unique())
    traces = []
    mean_df = songs_bill_melt.groupby(['old','bill_year'])[oldest_first_value].mean().reset_index()

    traces.append(dict(
        x=mean_df[mean_df['old']]['bill_year'],
        y=mean_df[mean_df['old']][oldest_first_value],
        # text=dfy_by_title_year['title_year'],
        mode='lines',
        marker={
            'size': 15,
            'opacity':0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name= 'Songs before 2000'
    ))
    traces.append(dict(
        x=mean_df[~mean_df['old']]['bill_year'],
        y=mean_df[~mean_df['old']][oldest_first_value],
        # text=dfy_by_title_year['title_year'],
        mode='lines',
        marker={
            'size': 15,
            'opacity':0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name='Songs after 2000'
    ))
    return {
        'data': traces,
        'layout': dict(
            title = 'The mean of song features throughout the years',
            xaxis={'title': 'Years'},
            yaxis={'title': 'Mean '+oldest_first_value,'range': [0.0, 1.0]},
            margin={'l': 180, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
        )
    }