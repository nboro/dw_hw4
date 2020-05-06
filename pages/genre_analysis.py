# load data
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

from app import app
# load data
sample_set = pd.read_csv("data/genre_analysis_set.csv")
specific = sample_set.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
specific = specific.rename(
    columns={
        "bill_year": "Ranking Year",
        "genre": "Genre",
        "bill_ranking": "Ranking",
        "release_year": "Released Year",
        "artist": "Artist",
        "title": "Title",
        "era": "Released Era"
    }
)
fig = px.line(
    specific,
    x="Ranking Year",
    y="Ranking",
    color="Released Era",
    line_group="Title",
    template="simple_white",
    facet_col="Genre",
    hover_name="Title",
    hover_data=["Artist", "Released Year"],
    title="Journeys of Top 10 most popular by Genre")

fig.update_traces(
    mode="markers+lines",
    marker={
        "line": {"width": 0.5, "color": "DarkSlateGrey"}
    }
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(xaxis_range=[2000,2020])

content = html.Div([
    dcc.Graph(figure=fig)
])
# available_genres = list(sample_set['genre'].unique())
# colors = ["#316fd4","#ed72e9","#4287f5","#4287f5","#b07633"]
# genre_colors = dict(zip(available_genres,colors))
# #genre_colors['All'] = '#ada5a5'
#
#
# content = html.Div(children=[
#     dcc.Dropdown(
#             id='inputid',
#             options=[{'label': i, 'value': i} for i in available_genres],
#             value='pop'),
#     dcc.Graph(id="genre_analysis")
#     ])
#
#
#
# @app.callback(Output(component_id='genre_analysis', component_property='figure'),
#               [Input(component_id='inputid', component_property='value')])
# def group_titles(value):
#     data = []
#     df = sample_set
#     # if value == "All":
#     #     specific = df.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
#     #     for namex, group in specific.groupby('title'):
#     #         data.append(go.Scatter(x=list(group.bill_year),
#     #                                y=list(group.bill_ranking),
#     #                                name=namex,
#     #                                visible=True, text=namex,
#     #                                #line=dict(color=genre_colors.get(value)),
#     #                                mode='lines+markers'))
#     #
#     # else:
#     specific = df.loc[sample_set['genre'] == value]
#     specific = specific.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
#     for namex, group in specific.groupby('title'):
#         data.append(go.Scatter(x=list(group.bill_year),
#                    y=list(group.bill_ranking),
#                    name=namex,
#                    visible=True, text=namex,
#                    line=dict(color=genre_colors.get(value)),
#                    mode='lines+markers'))
#     return {'data': data,
#             'layout': {
#                 'xaxis_range': {'min': '1999',
#                                 'max': '2020'},
#                 'xaxis_range': {'min': '0',
#                                 'max': '1000'},
#                 'yaxis': {
#                     'autorange': 'reversed'
#                 }
#             }
#             }


