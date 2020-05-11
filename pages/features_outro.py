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

