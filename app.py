import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from view import layout
from data import songs_bill_melt

app = dash.Dash(
    __name__,meta_tags=[{'name': 'viewport', 'content': 'width=device-width',
    # 'title':'Nemania Borovits | HW3 Data Visualization | MPG Dataset',
    # 'keywords':'Nemania Borovits, python dash, data visualization',
    # 'description':'Nemania Borovits made this simple python dash app as part of hw3 for data visualization course'
    }],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server
app.title = 'HW4 Data Visualization | Top 2000 Dataset'
app.layout = layout

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

if __name__ == '__main__':
    app.run_server(debug=True, port=80)
