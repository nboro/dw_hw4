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

fig = make_subplots(rows=1, cols=3, shared_yaxes=True, subplot_titles=('Rock', 'Pop', 'Soul'))

title = "Most Popular Songs in each Genre"

description = html.Div(children=[
    html.H5("Does era influence popularity ?", className="text-info"),
    dcc.Markdown([
        """
        As we can see songs released in the 2000’s don't make it to the top 100 in **Rock** but do in both **Pop** and **Soul**. 
        The top of the chart in **Pop** is often dominated by songs released in the 2000's. 
        For **Soul** the songs that were released in the 90’s never made it even into the top 1000 in the billboard over the last 20 years.    
        """,

    ]),
    html.P([
        """
        These graphs help discover how the era in which the songs were released causes a unique billboard journey within 
        a genre but varies significantly among each genre. Every genre has its dominating and inferior era's that keeps songs 
        ranked within its distinct ranges.      
        """

    ]),
])

def grouped_df(value):
    specific = sample_set.loc[sample_set['genre'] == value]
    specific = specific.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
    return specific


def group_titles():
    i = 1
    legend_names = set()
    for genree in ['rock', 'pop', 'soul']:
        specific = grouped_df(genree)
        for namex, group in specific.groupby('title'):
            era = group.era[0]
            era_year = group.era_year[0]
            line_color = era_col.get(str(era))
            fig.add_trace(go.Scatter(x=list(group.bill_year),
                                     y=list(group.bill_ranking),
                                     legendgroup=era_year,
                                     name=era_year,
                                     visible=True, text=namex,
                                     line=dict(width=2, color=line_color), showlegend=era_year not in legend_names,
                                     mode='lines', hoverinfo='x+y+text+name'),
                          row=1, col=i)
            legend_names.add(era_year)
        i += 1


# get template
graph_settings = get_graph_template()
graph_settings["layout"]["margin"]["t"] = 50
graph_settings["layout"]["legend"] = {
    "x": 0.5,
    "y": -0.1,
    "xanchor": "center",
    "yanchor": "top",
    "orientation": "h"
}
fig.update_layout(graph_settings["layout"],
                  yaxis_title="Billboard ranking")
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
