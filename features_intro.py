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
    html.H5("Measuring lyric diversity across different genres and song eras", className="text-info"),
    html.P("""
        This chart represents songs' similarity based on their lyrics. 
        Each dot is a song and the closer they are in the graph, 
        the more similar the lyrics are. 
    """),
    html.P("""
        Similarity is measured by converting the words in the lyrics to number representation with embeddings and PCA,
        for nerds go see this page (put a link here)
    """),
    html.P("""
        For instance, Bohemian Rhapsody is more similar to Imagine than Child in Time. 
        Child in Time is far from the center, 
        which indicates low degree of similarity with the rest of the songs in 1999. 
    """),
    html.H5("Try it yourself!", className="text-info"),
    html.P("""
        What happened over the ranking years? Are there more outlier songs or mainstream ones? 
        Do you see the same trend for Dutch songs? How about other genres?
    """)
])

