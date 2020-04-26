# import pandas as pd
# import pickle
import dash
import dash_bootstrap_components as dbc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# from view import layout
# from data import songs_bill_melt

app = dash.Dash(
    __name__,meta_tags=[{'name': 'viewport', 'content': 'width=device-width',
    # 'title':'Nemania Borovits | HW3 Data Visualization | MPG Dataset',
    # 'keywords':'Nemania Borovits, python dash, data visualization',
    # 'description':'Nemania Borovits made this simple python dash app as part of hw3 for data visualization course'
    }],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server
app.title = 'HW4 Data Visualization | Top 2000 Dataset'
# app.layout = layout
app.config.suppress_callback_exceptions = True
