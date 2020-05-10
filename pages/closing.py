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
    html.P("""
    We scraped wikipedia, process by, bla bla bla.
    """),
    html.P("""
    Graph created with Plotly, bla bla bla
    """),
    html.P("""
    Images taken from...
    """),
    html.H5("Composed by", className="text-info"),
    html.Ul([
        html.Li(dcc.Link("Chris Papas", href="https://www.linkedin.com/in/christos-papas-a2ba76172/")),
        html.Li(dcc.Link("Hameez Ariz", href="https://www.linkedin.com/in/hameez-ariz/")),
        html.Li(dcc.Link("Nemania Borovits", href="https://www.linkedin.com/in/nemania-borovits-8306b812a/")),
        html.Li(dcc.Link("Yosef Winatmoko", href="https://www.linkedin.com/in/yosef-ardhito-winatmoko-053a5754/")),
    ])
])
