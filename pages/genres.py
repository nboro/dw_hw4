import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


def get_highlight_line(row):
    if row["title"] == "Black":
        return 1
    elif row["title"] == "Jolene":
        return 2
    elif row["title"] == "In the end":
        return 3
    else:
        return 0


genre_df = pd.read_csv("data/bill_join_df.csv", index_col=0)
genre_df["group_genre"] = genre_df["main_genre"].apply(lambda g: g if g in ["rock", "pop", "others"] else "others")

all_genre_specific_df = pd.DataFrame()
for genre in ["rock", "pop", "others"]:
    # get billboard of each genre
    genre_specific_df = genre_df[genre_df["group_genre"] == genre].copy()
    genre_specific_df["genre_rank"] = genre_specific_df.groupby("bill_year")["bill_rank"].rank(method="first")
    rank_in_2019 = genre_specific_df[genre_specific_df["bill_year"] == 2019][["title", "genre_rank"]].rename(
        columns={"genre_rank": "rank_in_2019"}
    )
    rank_in_2019["rank_in_2019"] = rank_in_2019["rank_in_2019"].astype(int)
    # get top 15 of 2019 for each genre
    titles = list(genre_specific_df[genre_specific_df["bill_year"] == 2019].sort_values("bill_rank").head(10)["title"].values)
    genre_specific_df = genre_specific_df[genre_specific_df["title"].isin(titles)]
    genre_specific_df = genre_specific_df.merge(rank_in_2019, how="left", on="title")
    all_genre_specific_df = pd.concat([all_genre_specific_df, genre_specific_df])

all_genre_specific_df["genre_rank_neg"] = -1 * all_genre_specific_df["genre_rank"]
all_genre_specific_df["group_genre"] = all_genre_specific_df["group_genre"].map(
    {
        "rock": "Rock",
        "pop": "Pop",
        "others": "Others"
    }
)
all_genre_specific_df["is_dutch"] = all_genre_specific_df["is_dutch"].apply(lambda c: "NL" if c else "Other")
all_genre_specific_df["highlight"] = all_genre_specific_df.apply(get_highlight_line, axis=1)
all_genre_specific_df = all_genre_specific_df.rename(
    columns={
        "rank_in_2019": "Rank in 2019",
        "bill_year": "Ranking Year",
        "group_genre": "Genre",
        "genre_rank_neg": "Ranking",
        "is_dutch": "Artist Country",
        "year": "Song Release Year",
        "artist": "Artist"
    }
)
fig = px.line(
    all_genre_specific_df,
    x="Ranking Year",
    y="Ranking",
    color="highlight",
    color_discrete_sequence=["#bdbdbd", "#e6550d", "#e6550d", "#e6550d"],
    line_group="title",
    template="simple_white",
    facet_col="Genre",
    hover_name="title",
    hover_data=["Artist", "Song Release Year"],
    title="Journeys of Top 15 by Genre"
)
fig.update_traces(
    mode="markers+lines",
    marker={
        "line": {"width": 1, "color": "DarkSlateGrey"}
    }
)
fig.update_layout(
    showlegend=False,
    width=1200,
    height=600
)
content = html.Div([
    dcc.Graph(figure=fig)
])
