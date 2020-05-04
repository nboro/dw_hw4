import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)

top_df = bill_join_df[bill_join_df["bill_rank"] <= 200][["artist", "title", "year", "is_dutch", "main_genre", "bill_rank", "bill_year"]].dropna()
top_df["bill_year_w_jitter"] = top_df["bill_year"].apply(lambda y: y + np.random.normal(0, 0.1))

year_chart_df = top_df.rename(columns={"year": "Song Release Year", "bill_year_w_jitter": "Ranking Year", "is_dutch": "Artist Country"})
# year_chart_df["main_genre"] = year_chart_df["main_genre"].apply(lambda c: "Pop" if c == 'pop' else "Other")
genre_list = year_chart_df["main_genre"].unique().tolist()
genre_list.append("All")
year_chart_df['Artist Country'] = year_chart_df['Artist Country'].map({True: 'Dutch', False: 'Non Dutch'})



#
# fig = px.scatter(
#                     year_chart_df,
#                     x="Ranking Year",
#                     y="Song Release Year",
#                     color="main_genre",
#                     template="simple_white",
#                     labels=year_chart_df.apply(lambda row: "f{row['artist']}, {row['title']} ({row['Song Release Year']})", axis=1),
#                     hover_name="title",
#                     hover_data=["artist"],
#                     title="Top 200 NPO Ranking by Release Year"
# )
# _ = fig.update_traces(opacity=0.6, marker={"line": {"width": 1, "color": "DarkSlateGrey"}})
# _ = fig.update_layout(
#     width=1200,
#     height=760
# )



content  = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Dropdown(
        id='genre-dropdown',
        options = [{'label': key, 'value': key} for key in genre_list ],
        value = 'All'
    ),
    # dcc.Slider(
    #     id='year-slider',
    #     min=year_chart_df.head(10)
    #     max=year_chart_df.head(200)
    #     value=df['year'].min(),
    #     marks={str(year): str(year) for year in df['year'].unique()},
    #     step=None
    # )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('genre-dropdown', 'value')])
def update_figure(selected_genre):
    if selected_genre != "All":
        filtered_year_chart_df = year_chart_df[year_chart_df.main_genre == selected_genre]
    else:
        filtered_year_chart_df = year_chart_df
    traces = []
    for i in filtered_year_chart_df['Artist Country'].unique():
        df = filtered_year_chart_df[filtered_year_chart_df['Artist Country'] == i]
        traces.append(dict(
            x=df["Ranking Year"],
            y=df["Song Release Year"],
            text= df["title"],
            mode='markers',
            # color=,
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'This is x title',
                   'range':[1998, 2020]},
            yaxis={'title': 'This is y title', 'range': [1950, 2020]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )
    }
