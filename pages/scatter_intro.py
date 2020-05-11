import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages.scatter import year_chart_df, isDutch_list, graph_settings
from copy import deepcopy


traces = []
filtered_df = year_chart_df[year_chart_df['title'].isin(["Jimmy", "Fix You"])]
for i in year_chart_df['main_genre'].unique():
    df = filtered_df[filtered_df['main_genre'] == i]
    custom_data = [
        (r["title"], r["artist"], r["bill_rank"], r["bill_year"], r["song_id"]) for idx, r in df.iterrows()
    ]
    traces.append(dict(
        type="scattergl",
        x=df["Ranking Year"],
        y=df["Song Release Year"],
        text=df["title"],
        hoverinfo='text',
        hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Rank=%{customdata[2]} (%{customdata[3]})',
        mode='markers',
        customdata=custom_data,
        opacity=0.7,
        marker={
            'size': 8,
            'line': {'width': 0.5, 'color': '#2B3E50'},
        },
        name=i
    ))

layout_settings = deepcopy(graph_settings["layout"])
layout_settings["annotations"] = [
    dict(
        x=2003,
        y=1976,
        xref="x",
        yref="y",
        text="Jimmy by Boudewijn de Groot",
        showarrow=False
    ),
    dict(
        x=2015,
        y=2008,
        xref="x",
        yref="y",
        text="Fix You by Coldplay",
        showarrow=False
    ),
]


title = "Release year of top-200 songs"

description = html.Div(children=[
    html.H5("Comparing the release year and the ranking year of songs", className="text-info"),
    html.P("""
        You can see at the plot on your left the yellow dots representing the "Jimmy" by "Boudejiwn de Groot". More specifiaclly, "Jimmy" was at the top-200 chart from 1999 until 2005 and at 2008. The yellow represent the genre of the song, which in this case is "rock"
    """),
    html.P("""
        The blue dots refer to "Fix You" by "Coldplay". The color of dots is blue because "Fix You" is categorized as pop. Moreover the song entered the chart in 2011, where it is until today.
    """),
    html.P("""
        If you 'hover' the mouse over the dot, you can see more info of the song.
    """),
    # html.P("""
    #     For instance, Bohemian Rhapsody is more similar to Imagine than Child in Time.
    #     Child in Time is far from the center,
    #     which indicates low degree of similarity with the rest of the songs in 1999.
    # """,className="text-justify"),
    html.H5("Explore on your own!", className="text-info"),
    html.P("""
         Do you want to learn more about the songs? Press the next button and start exploring! You can filter from the top-10 to top-200 songs. You can filter to see only Dutch songs or only International songs. Last but not least, you can filter the genders!
    """)
])

content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Country:"),
                dbc.Select(
                    id='isDutch-dropdown-intro',
                    options=[{'label': key, 'value': key} for key in isDutch_list],
                    value='All',
                    disabled=True
                )
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='scatter-intro',
                figure={
                    'data': traces,
                    'layout': layout_settings
                },
                config=graph_settings["config"])
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label(children="Top-n:"),
            dcc.Slider(
                id='rank-slider-intro',
                min=10,
                max=200,
                value=200,
                marks={str(pos): str(pos) for pos in range(10, 201, 10)},
                step=10,
                disabled=True
            ),
        ])
    ])
]

# description = html.Div([html.H5("Lorem Ipsum")])

# html.H5("Popular songs by Genre", className="text-info"),
#     html.P([
#         """
#         This chart visualizes the billboard ranking journey of the most popular songs in 2020 segregated by the top three genres.
#         Within each chart the songs have been color coordinated by the era in which the songs were released. Each line in the chart
#         is a song that made it into the billboard charts between 1999 to 2019 and their respective ranking each year.
#         """
#     ]),
#     html.H6("The color of the lines.", className="text-info"),
#     html.P([
#         """
#         The songs have been categorised into three eras (oldies, 2000’s & 90’s) based on the year that it was released,
#         which could give us more insight into why a song is more or less popular within a genre.
#         """
#     ]),
