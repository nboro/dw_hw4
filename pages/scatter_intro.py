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

description = html.Div([html.P("Lorem Ipsum")])
