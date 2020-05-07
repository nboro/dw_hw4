import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import get_graph_template
from app import app

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)

top_df = bill_join_df[bill_join_df["bill_rank"] <= 200][["artist", "title", "year", "is_dutch", "main_genre", "bill_rank", "bill_year"]].dropna()
top_df["bill_year_w_jitter"] = top_df["bill_year"].apply(lambda y: y + np.random.normal(0, 0.1))

year_chart_df = top_df.rename(columns={"year": "Song Release Year", "bill_year_w_jitter": "Ranking Year", "is_dutch": "Artist Country"})
year_chart_df['main_genre'] = year_chart_df['main_genre'].apply(lambda g: g if g in ["rock", "pop"] else "others")
genre_list = year_chart_df["main_genre"].unique().tolist()
genre_list.append("All")

year_chart_df['Artist Country'] = year_chart_df['Artist Country'].map({True: 'Dutch', False: 'Non Dutch'})
isDutch_list = year_chart_df['Artist Country'].unique().tolist()
isDutch_list.append("All")

bill_rank_list = year_chart_df["bill_rank"].sort_values().unique().tolist()

graph_settings = get_graph_template()
graph_settings["layout"]["xaxis"]["title"] = "Ranking Year"
graph_settings["layout"]["xaxis"]["range"] = [1998, 2020]
graph_settings["layout"]["yaxis"]["title"] = "Song Release Year"
graph_settings["layout"]["yaxis"]["range"] = [1955, 2020]


content = html.Div([

    dbc.Row([
        dbc.Col(html.Div([
            html.H2("Release year of top-200 songs")
        ]),className="text-center"),
    ]),

    dbc.Row([

                dbc.Col(html.Div([
                    dcc.Graph(id='graph-with-slider'),

                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H6("Filter by top k songs")
                        ]), className="text-center", ),


                    ]),

                    dcc.Slider(
                            id='rank-slider',
                            min=10,
                            max=200,
                            value=200,
                            marks={str(pos): str(pos) for pos in range(10,201,10)},
                            step=10,

                    ),

                ])),


                dbc.Col(html.Div([
                    dcc.Dropdown(
                        id='isDutch-dropdown',
                        options=[{'label': key, 'value': key} for key in isDutch_list],
                        value='All')
                ]),width={"size":3,"order":2,"offset": 0}),
    ]),

    # dbc.Row(
    #     [
    #         dbc.Col(html.Div(children=[
    #                     dcc.Slider(
    #                         id='rank-slider',
    #                         min=10,
    #                         max=200,
    #                         value=200,
    #                         marks={str(pos): str(pos) for pos in range(10,211,20)},
    #                         step=10,
    #
    #                     ),
    #         ])),
    #         dbc.Col(id='feature_text', width="auto", align="center")
    #     ],
    #     justify="center",
    # )
    ],
    style={'margin-top':'20px'}),


    # html.Div(
    #     [
    #         dcc.Graph(id='graph-with-slider',style={'width': '70%'}),
    #
    #         dcc.Dropdown(
    #             id='isDutch-dropdown',
    #             options=[{'label': key, 'value': key} for key in isDutch_list],
    #             value='All'
    #         ),
    #
    #         dcc.Slider(
    #             id='rank-slider',
    #             min=10,
    #             max=200,
    #             value=200,
    #             marks={str(pos): str(pos) for pos in range(10,211,20)},
    #             step=10,
    #
    #         ),
    #
    #     ],
    #     style={'width': '100%',
    #            'display': 'inline-block'}),
# ])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('isDutch-dropdown', 'value'),
     Input('rank-slider', 'value')
     ])
def update_figure(selected_isDutch, bill_rank_lista):
    if selected_isDutch != "All":
        filtered_year_chart_df = year_chart_df[year_chart_df['Artist Country'] == selected_isDutch]
    else:
        filtered_year_chart_df = year_chart_df

    filtered_year_chart_df = filtered_year_chart_df[filtered_year_chart_df["bill_rank"] <= bill_rank_lista]

    traces = []
    for i in filtered_year_chart_df['main_genre'].unique():
        df = filtered_year_chart_df[filtered_year_chart_df['main_genre'] == i]
        traces.append(dict(
            x=df["Ranking Year"],
            y=df["Song Release Year"],
            text= df["title"],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 8,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))



    return {
        'data': traces,
        'layout': graph_settings["layout"]
        # 'layout': dict(
        #     xaxis={'title': 'Ranking Year',
        #            'range':[1998, 2020]},
        #     yaxis={'title': 'Song Release Year', 'range': [1955, 2020]},
        #     margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        #     legend={'x': 0, 'y': 1},
        #     hovermode='closest',
        # )
    }
