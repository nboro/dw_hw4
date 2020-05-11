import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app

title = "What's next?"

content = dbc.Row(children=[
    html.H4("Lorem Ipsum", className="text-info"),
    html.P("""
    Illum eius voluptatem nulla mollitia. Dolores doloremque est et atque molestiae dolor. Aut tempore aut quo ratione saepe animi repudiandae illo. Pariatur quia sequi id repudiandae porro dolor. Consequatur sint molestias assumenda rerum qui incidunt consequatur dignissimos.
    """),
    html.P("""
    Necessitatibus ut quibusdam qui illo quae asperiores suscipit. Dicta expedita dolorem dolore. Velit eligendi in minima temporibus commodi cumque. Aliquid adipisci velit repellendus. Non velit excepturi quam necessitatibus nihil reprehenderit non id. Blanditiis ducimus et aut iste veritatis.
    """),
    html.H4("Lorem Ipsum", className="text-info"),
    html.P("""
    Illum eius voluptatem nulla mollitia. Dolores doloremque est et atque molestiae dolor. Aut tempore aut quo ratione saepe animi repudiandae illo. Pariatur quia sequi id repudiandae porro dolor. Consequatur sint molestias assumenda rerum qui incidunt consequatur dignissimos.
    """),
    html.P("""
    Necessitatibus ut quibusdam qui illo quae asperiores suscipit. Dicta expedita dolorem dolore. Velit eligendi in minima temporibus commodi cumque. Aliquid adipisci velit repellendus. Non velit excepturi quam necessitatibus nihil reprehenderit non id. Blanditiis ducimus et aut iste veritatis.
    """),
    dbc.Row([
        dbc.Col(
            html.Img(
                src=app.get_asset_url('imgs/bob.png'),
                className="img-fluid mx-auto d-block"
            ),
            width=3
        ),
        dbc.Col([
            html.Div([
                html.Em("One good thing about music,"), html.Br(),
                html.Em("when it hits you, you feel no pain.")
            ]),
            html.Div(
                "- Bob Marley"
            )
        ],
            width=4
        ),
    ])
])

description = html.Div([
    html.H5("Data & Methodology", className="text-info"),
    html.P([
        "The ranking data is based on ",
        dcc.Link("NPO Radio 2 Top 2000", href="https://www.nporadio2.nl/top2000"),
        " and retrieved via the corresponding ",
        dcc.Link("Wikipedia page",
                 href="https://nl.wikipedia.org/wiki/Lijst_van_Radio_2-Top_2000%27s"),
        ". Song features are gathered with ",
        dcc.Link("Spotify API",
                 href="https://developer.spotify.com/documentation/web-api/quick-start/"),
        " using the ",
        dcc.Link("spotipy", href="https://github.com/plamere/spotipy"),
        " library."
    ]),
    html.P([
        "Lyrics are collected from ",
        dcc.Link("lyrics.wikia.com", href="http://lyrics.wikia.com/"),
        " using the ",
        dcc.Link("lyricwikia", href="https://pypi.org/project/lyricwikia/"),
        " library and ",
        dcc.Link("musixmatch", href="https://www.musixmatch.com/"),
        ". We use pre-train embeddings from ",
        dcc.Link("Google", href="https://code.google.com/archive/p/word2vec/"),
        " for the English songs and ",
        dcc.Link("dutchembeddings", href="https://github.com/clips/dutchembeddings"),
        " for Dutch."
    ]),
    html.P([
        "Visuals developed with ",
        dcc.Link("Dash", href="https://plotly.com/dash/"),
        " and hosted in ",
        dcc.Link("Heroku", href="https://www.heroku.com/"),
        ". Website template is based on ",
        dcc.Link("Bootswatch", href="https://bootswatch.com/"),
        "."
    ]),
    html.H5("Composed by", className="text-info"),
    html.Ul([
        html.Li(dcc.Link("Chris Papas", href="https://www.linkedin.com/in/christos-papas-a2ba76172/")),
        html.Li(dcc.Link("Hameez Ariz", href="https://www.linkedin.com/in/hameez-ariz/")),
        html.Li(dcc.Link("Nemania Borovits", href="https://www.linkedin.com/in/nemania-borovits-8306b812a/")),
        html.Li(dcc.Link("Yosef Winatmoko", href="https://www.linkedin.com/in/yosef-ardhito-winatmoko-053a5754/")),
    ])
])
