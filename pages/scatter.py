import numpy as np
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
top_df = bill_join_df[bill_join_df["bill_rank"] <= 200][
    ["artist", "title", "year", "is_dutch", "main_genre", "bill_rank", "bill_year"]].dropna()
top_df["bill_year_w_jitter"] = top_df["bill_year"].apply(lambda y: y + np.random.normal(0, 0.1))
year_chart_df = top_df.rename(
    columns={
        "year": "Song Release Year",
        "bill_year_w_jitter": "Ranking Year",
        "is_dutch": "Artist Country"
    }
)
year_chart_df["Artist Country"] = year_chart_df["Artist Country"].apply(lambda c: "NL" if c else "Other")
fig = px.scatter(
    year_chart_df,
    x="Ranking Year",
    y="Song Release Year",
    color="Artist Country",
    template="simple_white",
    labels=year_chart_df.apply(lambda row: "f{row['artist']}, {row['title']} ({row['Song Release Year']})", axis=1),
    hover_name="title",
    hover_data=["artist"],
    title="test test 1-2"
)
fig.update_traces( opacity=0.6, marker={"line": {"width": 1, "color": "DarkSlateGrey"}} )
fig.update_layout(
    width=1200,
    height=760
)
content = html.Div([
    dcc.Graph(figure=fig)
])
