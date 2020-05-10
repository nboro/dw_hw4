# load data
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from utils import get_graph_template

from app import app
# load data
sample_set = pd.read_csv("data/genre_analysis_v2.csv")
# Set color for Era's
available_eras = list(sample_set['era'].unique())
era_col = {
    "oldies": "#f0ad4e",
    "90s": "#5bc0de",
    "2000s": "#d9534f"
}

fig = make_subplots(rows=1, cols=3, shared_yaxes=True, subplot_titles=('Rock', '', ''))

title = "Most Popular Songs in each Genre"

description = html.Div([html.P("Lorem Ipsum")])

def grouped_df(value):
    specific = sample_set.loc[sample_set['genre'] == value]
    specific = specific.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
    return specific


def group_titles():
    i = 1
    legend_names = set()
    for genree in ['rock']:
        specific = grouped_df(genree)
        for namex, group in specific.groupby('title'):
            era = group.era[0]
            line_color = era_col.get(str(era))
            fig.add_trace(go.Scatter(x=list(group.bill_year),
                                     y=list(group.bill_ranking),
                                     legendgroup=era,
                                     name=era,
                                     visible=True, text=namex,
                                     line=dict(width=2, color=line_color), showlegend=era not in legend_names,
                                     mode='lines', hoverinfo='x+y+text+name'),
                          row=1, col=i)
            legend_names.add(era)
        i += 1


# get template
graph_settings = get_graph_template()
graph_settings["layout"]["margin"]["t"] = 50
graph_settings["layout"]["legend"] = {
    "x": 0,
    "y": -0.1,
    "xanchor": "left",
    "yanchor": "top",
    "orientation": "h"
}
fig.update_layout(graph_settings["layout"])
fig.update_xaxes(
    range=[1998, 2020],
    color="#EBEBEB",
    showgrid=False,
    automargin=True,
    tickmode="array",
    tickvals=[2000, 2010, 2020]
)
fig.update_yaxes(
    range=[2050, 0],
    color="#EBEBEB",
    gridcolor="#4E5D6C",
    automargin=True,
    zeroline=False,
    tickmode="array",
    tickvals=[50, 250, 500, 1000, 2000]
)
group_titles()
content = html.Div([
    dcc.Graph(figure=fig, config=graph_settings["config"])
])