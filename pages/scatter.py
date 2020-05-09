import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import get_graph_template, get_song_card
from app import app

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)

top_df = bill_join_df[bill_join_df["bill_rank"] <= 200][
    ["song_id", "artist", "title", "year", "is_dutch", "main_genre", "bill_rank", "bill_year"]].dropna()
top_df["bill_year_w_jitter"] = top_df["bill_year"].apply(lambda y: y + np.random.normal(0, 0.1))

year_chart_df = top_df.rename(
    columns={"year": "Song Release Year", "bill_year_w_jitter": "Ranking Year", "is_dutch": "Artist Country"})
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
graph_settings["layout"]["legend"] = {
    "x": 0,
    "y": 1
}

title = "Release year of top-200 songs"

content = [
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                dbc.Label("Country:"),
                dbc.Select(
                    id='isDutch-dropdown',
                    options=[{'label': key, 'value': key} for key in isDutch_list],
                    value='All'
                )
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph-with-slider',
                figure={"data": [], "layout": graph_settings["layout"]},
                config=graph_settings["config"])
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label(children="Top-n:"),
            dcc.Slider(
                id='rank-slider',
                min=10,
                max=200,
                value=200,
                marks={str(pos): str(pos) for pos in range(10, 201, 10)},
                step=10,
            ),
        ])
    ])
]

description = html.Div(id='scatter-description', children="Click a song to see details.")


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


@app.callback(Output("scatter-description", "children"), [Input("graph-with-slider", "clickData")])
def display_artist(clickData):
    #if clickData:
    #
    # titlos = click['customdata'][0]
    # rankyear = round(click['x'])
    # billrank = click['customdata'][1]
    #
    # row1 = html.Tr([html.Td(dcc.Markdown('''**Title is**''')), html.Td(titlos)])
    # row2 = html.Tr([html.Td(dcc.Markdown('''**Rank Year**''')), html.Td(rankyear)])
    # row3 = html.Tr([html.Td(dcc.Markdown('''**Bill Rank**''')), html.Td(billrank)])
    # table_body = [html.Tbody([row1,row2,row3])]
    # table = dbc.Table(table_body
    # return html.Div(children=[
    #     table
    # ], className="table-responsive")
    if clickData is None or "customdata" not in clickData["points"][0]:
        return [html.Div("Click a song to see details.")]

    click = clickData['points'][0]
    song_id = click["customdata"][4]
    return get_song_card(song_id)
