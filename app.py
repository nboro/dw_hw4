import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from view import layout
from data import selected_songs,feature_list

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
    Output('song-feature-graph', 'figure'),
    [Input('xaxis-column', 'value')])
def update_graph(xaxis_value):
    df = selected_songs[['title','year','title_year',xaxis_value]]
    traces = []
    traces.append(dict(
        x=df[xaxis_value],
        y=df['title_year'],
        # text=df_by_country['car name'],
        # customdata = df_by_country['year'],
        type='bar',
        opacity=0.7,
        width = 0.9,
        orientation='h'
        # name=i
    ))
    return {
        'data': traces,
        'layout': dict(
            title = 'Song features of Top 15 for 2019',
            xaxis={'type': 'Linear', 'title': '', 'range': [0.0, 1.0]},
            yaxis={'title': ''},
            margin={'l': 180, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1, # gap between bars of the same location coordinate.
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True, port=80)
