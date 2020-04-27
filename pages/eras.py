import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
bill_join_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
song_features = [
    'duration_ms', 'followers', 'analysis_loudness', 'analysis_tempo',
    'feature_danceability', 'feature_energy', 'feature_speechiness', 'feature_instrumentalness',
    'feature_liveness', 'feature_valence'
]
era_df = bill_join_df[["title", "era", "hp", "artist"]].groupby(["title", "era", "hp"]).count().reset_index().rename(
    columns={"artist": "count"}
)
era_df["era_rank"] = era_df.groupby("era")["hp"].rank(method="first")
best_era_df = bill_join_df[bill_join_df["title"].isin(era_df[era_df["era_rank"] < 200]["title"].unique())].copy()
best_era_df = best_era_df[["title", "era"] + song_features].dropna().reset_index()
first_title_df = best_era_df[["index", "title"]].groupby("title")["index"].rank(method="first")
best_era_df = best_era_df[first_title_df == 1]
del best_era_df["index"]
del best_era_df["title"]
best_era_df.columns = [
    "era", "Duration", "Mainstream", "Loudness", "Tempo",
    "Danceability", "Energy", "Speechiness", "Instrumentalness",
    "Liveness", "Valence"
]
all_cols = list(best_era_df.columns.values)
best_era_df = best_era_df.groupby("era").mean().reset_index().melt(id_vars=["era"])
compare_oldies_df = best_era_df[best_era_df["era"] == "oldies"][["variable", "value"]].rename(columns={"value": "value_oldies"})
best_era_df = best_era_df.merge(compare_oldies_df, how="left", on="variable")
best_era_df["relative_to_oldies"] = (best_era_df["value"] - best_era_df["value_oldies"]) * 100 / best_era_df["value_oldies"]
best_era_df["era"] = best_era_df["era"].map({"oldies": "1920-1980", "90s": "1980-1990", "2000s": "1990-2020"})
best_era_df = best_era_df[["era", "variable", "relative_to_oldies"]].sort_values(["era", "relative_to_oldies"])
best_era_df.columns = ["Song Era", "Song Features", "Compared to Oldies (Song Released < 1990)"]
fig = px.scatter(
    best_era_df, x=best_era_df.columns[2], y=best_era_df.columns[1],
    color="Song Era",
    title="Song Features Throughout Eras",
    template="plotly_white",
    hover_name=best_era_df.columns[2],
    color_discrete_sequence=["#bdbdbd", "#9ecae1", "#3182bd"],
)
fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))
fig.update_layout(
    title="Comparing Features of Different Song Eras (based on Spotify API)",
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=25,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)',
        ticksuffix='%'
    ),
    margin=dict(l=140, r=40, b=50, t=80),
    legend=dict(
        font_size=10,
        yanchor='middle',
        xanchor='right',
    ),
    width=1024,
    height=760,
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='closest',
)
content = html.Div([
    dcc.Graph(figure=fig)
])
