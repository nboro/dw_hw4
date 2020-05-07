# load data
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from app import app
# load data
sample_set = pd.read_csv("data/genre_analysis.csv")
# Set color for Era's
available_eras = list(sample_set['era'].unique())
era_colors = ["#ff1100", "#16c1c4", "#26b812"]
era_col = dict(zip(available_eras, era_colors))

fig = make_subplots(rows=1, cols=3, subplot_titles=('Genre: Pop', 'Genre: Rock', 'Genre: Other'))


def grouped_df(value):
    specific = sample_set.loc[sample_set['genre'] == value]
    specific = specific.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
    return specific


def group_titles():
    pop_specific = grouped_df('pop')
    i = 1
    for genree in ['pop', 'rock', 'other']:
        specific = grouped_df(genree)
        for namex, group in specific.groupby('title'):
            era = group.era[0]
            line_color = era_col.get(str(group.era[0]))
            fig.add_trace(go.Scatter(x=list(group.bill_year),
                                     y=list(group.bill_ranking),
                                     name=group.era[0],
                                     visible=True, text=namex,
                                     line=dict(color=line_color), showlegend=True,
                                     mode='lines+markers', hoverinfo='x+y+text+name'),
                          row=1, col=i)
        i += 1


fig.update_yaxes(autorange="reversed")

fig.update_layout(xaxis_range=[1999, 2020])

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)

group_titles()
# specific = sample_set.groupby('title_index').apply(pd.DataFrame.sort_values, 'bill_year', ascending=True)
# specific = specific.rename(
#     columns={
#         "bill_year": "Ranking Year",
#         "genre": "Genre",
#         "bill_ranking": "Ranking",
#         "release_year": "Released Year",
#         "artist": "Artist",
#         "title": "Title",
#         "era": "Released Era"
#     }
# )
# fig = px.line(
#     specific,
#     x="Ranking Year",
#     y="Ranking",
#     color="Released Era",
#     line_group="Title",
#     template="simple_white",
#     facet_col="Genre",
#     hover_name="Title",
#     hover_data=["Artist", "Released Year"],
#     title="Journeys of Top 10 most popular by Genre")
#
# fig.update_traces(
#     mode="markers+lines",
#     marker={
#         "line": {"width": 0.5, "color": "DarkSlateGrey"}
#     }
# )
# fig.update_yaxes(autorange="reversed")
# fig.update_layout(xaxis_range=[2000,2020])

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


