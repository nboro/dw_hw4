import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from view import layout
from data import selected_songs19,selected_songs99

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
    Output('song-feature-19', 'figure'),
    [Input('oldest-first', 'value'),
    Input('oldest-second', 'value')])
def update_graph19(oldest_first_value,oldest_second_value):

    dfx = selected_songs19[['title','year','title_year',oldest_first_value]]
    dfy = selected_songs19[['title','year','title_year',oldest_second_value]]

    traces = []
    for i in selected_songs19.title_year.unique():
        dfx_by_title_year = dfx[dfx['title_year'] == i]
        dfy_by_title_year = dfy[dfy['title_year'] == i]
        traces.append(dict(
            x=dfx_by_title_year[oldest_first_value],
            y=dfy_by_title_year[oldest_second_value],
            text=dfy_by_title_year['title_year'],
            mode='markers',
            marker={
                'size': 15,
                'opacity':0.7,
                'line': {'width': 0.5, 'color': 'white'}
            },
        name=i
        ))
    return {
        'data': traces,
        'layout': dict(
            title = 'Song features of Top 15 for 2019',
            xaxis={'title': oldest_first_value, 'range': [0.0, 1.0]},
            yaxis={'title': oldest_second_value},
            margin={'l': 180, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
        )
    }
@app.callback(
    Output('song-feature-99', 'figure'),
    [Input('oldest-first', 'value'),
    Input('oldest-second', 'value')])
def update_graph99(oldest_first_value,oldest_second_value):

    dfx = selected_songs99[['title','year','title_year',oldest_first_value]]
    dfy = selected_songs99[['title','year','title_year',oldest_second_value]]

    traces = []
    for i in selected_songs99.title_year.unique():
        dfx_by_title_year = dfx[dfx['title_year'] == i]
        dfy_by_title_year = dfy[dfy['title_year'] == i]
        traces.append(dict(
            x=dfx_by_title_year[oldest_first_value],
            y=dfy_by_title_year[oldest_second_value],
            text=dfy_by_title_year['title_year'],
            mode='markers',
            marker={
                'size': 15,
                'opacity':0.7,
                'line': {'width': 0.5, 'color': 'white'}
            },
        name=i
        ))
    return {
        'data': traces,
        'layout': dict(
            title = 'Song features of Top 15 for 1999',
            xaxis={'title': oldest_first_value, 'range': [0.0, 1.0]},
            yaxis={'title': oldest_second_value},
            margin={'l': 180, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=80)
