import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

from dash.dependencies import Output, Input

from utils import create_initial_era_df,create_era_df,get_max_each_feature,get_graph_template,get_song_card_feature
from app import app

content = [

]

title = "Comparing Features of Different Song Eras (based on Spotify API)"

description = html.Div(children=[
    html.H5("Identifying song characteristics among eras", className="text-info"),
    html.P("""
        In order to validate our hypothesis about the preference for older songs we additionally leveraged information from spotify. More specifically, for each song in our dataset we retrieved quantitative measures for 9 song features from spotify API. 
    """,className="text-justify"),
    html.P("""
        In order  to utilize these features more effectively we split the dataset into 3 eras and then computed the mean value for each feature for every era. To better communicate our findings we calculated the difference between the oldest era and the two other eras.
    """,className="text-justify"),
    # html.P("""
    #     For instance, Bohemian Rhapsody is more similar to Imagine than Child in Time. 
    #     Child in Time is far from the center, 
    #     which indicates low degree of similarity with the rest of the songs in 1999. 
    # """,className="text-justify"),
    html.H5("Try it yourself!", className="text-info"),
    html.P("""
        Does the song feature information provide eventually insights regarding our hypothesis…? Do these insights align for dutch songs and international songs…? Can we combine information from two or more features…?
    """,className="text-justify")
])