from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils import get_nav_buttons
from app import app
from pages import scatter, genre_analysis, features, lyrics

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([
                html.H3(id="title", children="")
            ]), className="text-center"),
        ]),
        dbc.Row([
            dbc.Col(id="navs", width=12, className="text-center")
        ]),
        dbc.Row([
            dbc.Col(
                id="content",
                children=[],
                width=9
            ),
            dbc.Col(
                id="description",
                children=[],
                width=3
            )
        ])
    ])
])

index = {
    "title": "We are here for a ride, darling.",
    "content": html.Img(src=app.get_asset_url('imgs/freddie.png'), className="img-fluid mx-auto"),
    "description": html.Div([
        dcc.Link('Main Scatter', href='/scatter'),
        html.Br(),
        dcc.Link('Genres', href='/genres'),
        html.Br(),
        dcc.Link('Song Features', href='/features'),
        html.Br(),
        dcc.Link('Lyrics', href='/lyrics')
    ])
}


@app.callback(
    [
        Output('title', 'children'),
        Output('content', 'children'),
        Output('description', 'children'),
        Output('navs', 'children')
    ],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == "/":
        return index["title"], index["content"], index["description"], \
               get_nav_buttons(None, "#", "oi-media-play", "/scatter")
    elif pathname == "/scatter":
        return scatter.title, scatter.content, scatter.description, \
               get_nav_buttons("oi-media-step-backward", "/", "oi-media-step-forward", "/genres")
    elif pathname == "/genres":
        return "Genres", genre_analysis.content, "", \
               get_nav_buttons("oi-media-step-backward", "/scatter", "oi-media-step-forward", "/features")
    elif pathname == "/features":
        return features.title, features.content, features.description, \
               get_nav_buttons("oi-media-step-backward", "/genres", "oi-media-step-forward", "/lyrics")
    elif pathname == "/lyrics":
        return lyrics.title, lyrics.content, lyrics.description, \
               get_nav_buttons("oi-media-step-backward", "/features", "oi-home", "/")
    return "404"


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
