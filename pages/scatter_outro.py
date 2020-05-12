
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages.scatter import year_chart_df, isDutch_list, graph_settings

traces = []
for i in year_chart_df['main_genre'].unique():
    df = year_chart_df[year_chart_df['main_genre'] == i]
    custom_data = [
        (r["title"], r["artist"], r["bill_rank"], r["bill_year"], r["song_id"]) for idx, r in df.iterrows()
    ]

    # ranking_year = str(df.iloc[0]["Ranking Year"])
    # bill_rank = df[0]['bill_rank']

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
            'line': {'width': 0.5, 'color': '#2B3E50'}
        },
        name=i
    ))

fig = {
    'data': traces,
    'layout': graph_settings["layout"]
}


title = "Release year of top-200 songs"

content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Country:"),
                dbc.Select(
                    id='isDutch-dropdown-outro',
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
                id='scatter-outro',
                figure=fig,
                config=graph_settings["config"])
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label(children="Top-n:"),
            dcc.Slider(
                id='rank-slider-outro',
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

description = html.Div(children=[
    html.H5("Let's discover some insights!", className="text-info"),
    html.P("""
        Wow! Lot of yellow dots! It is clear that rock music is dominating, especially the old songs. So, we notice that Dutch people prefer "rock" over other genres. 
    """),
    html.P("""
        However, it is noticeable at the top right corner lot of blue dots. If we properly filter, we notice that after 2010, the amount of songs that entered the charts were more "pop" than "rock".
    """),
    html.P("""
        Is everything that is mentioned above true for both "Dutch" and "International" music? Well, for international music we can see the same patterns. Especially for "pop", after 2010 is almost the dominant genre.
        On the other hand, "Dutch" songs does not seem to follow this pattern. We notice that dutch songs that joined the charts the last few years are still "rock". 
    """),

])
