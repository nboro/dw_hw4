from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils import get_nav_buttons
from app import app
from pages import (
    opening,
    scatter,
    genre_analysis,
    features,features_intro,features_outro,
    lyrics, lyrics_intro, lyrics_outro,
    closing
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([
                html.H3(id="title", children=""),
                html.Div(id="navs")
            ]), className="text-center"),
        ]),
        dbc.Row([
            dbc.Col(
                id="content",
                children=[],
                width=9
            ),
            dbc.Col(id="description", width=3)
        ]),
    ])
])


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
        return opening.title, opening.content, opening.description, \
               get_nav_buttons(None, "#", "oi-media-play", "/scatter")
    elif pathname == "/scatter":
        return scatter.title, scatter.content, scatter.description, \
               get_nav_buttons("oi-media-step-backward", "/", "oi-media-step-forward", "/genres")
    elif pathname == "/genres":
        return "Genres", genre_analysis.content, "", \
               get_nav_buttons("oi-media-step-backward", "/scatter", "oi-media-step-forward", "/features")
    elif pathname == "/features/intro":
        return features_intro.title, features_intro.content, features_intro.description, \
               get_nav_buttons("oi-media-step-backward", "/genres", "oi-media-step-forward", "/lyrics/intro")
    elif pathname == "/features/reff":
        return features.title, features.content, features.description, \
               get_nav_buttons("oi-media-step-backward", "/genres", "oi-media-step-forward", "/lyrics/intro")
    elif pathname == "/features/outro":
        return features_outro.title, features_outro.content, features_outro.description, \
               get_nav_buttons("oi-media-step-backward", "/genres", "oi-media-step-forward", "/lyrics/intro")
    elif pathname == "/lyrics/intro":
        return lyrics_intro.title, lyrics_intro.content, lyrics_intro.description, \
               get_nav_buttons("oi-media-step-backward", "/features", "oi-media-step-forward", "/lyrics/reff")
    elif pathname == "/lyrics/reff":
        return lyrics.title, lyrics.content, lyrics.description, \
               get_nav_buttons("oi-media-step-backward", "/lyrics/intro", "oi-media-step-forward", "/lyrics/outro")
    elif pathname == "/lyrics/outro":
        return lyrics_outro.title, lyrics_outro.content, lyrics_outro.description, \
               get_nav_buttons("oi-media-step-backward", "/lyrics/reff", "oi-media-step-forward", "/encore")
    elif pathname == "/encore":
        return closing.title, closing.content, closing.description, \
               get_nav_buttons("oi-media-step-backward", "/lyrics/outro", "oi-home", "/")
    return opening.title, opening.content, opening.description, get_nav_buttons(None, "#", "oi-media-play", "/scatter")


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
