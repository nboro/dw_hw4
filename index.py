from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from app import app
from pages import scatter, genres, eras, features, lyrics
from navbar import Navbar

nav = Navbar()



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[
        dcc.Link("<< PREV", id="prev-page", href="#"),
        "|",
        dcc.Link("HOME", id="home-page", href="/"),
        "|",
        dcc.Link("NEXT >>", id="next-page", href="#")
    ]),
    html.Div(id='page-content')
])

index = html.Div([
    dcc.Link('Main Scatter', href='/scatter'),
    html.Br(),
    dcc.Link('Genres', href='/genres'),
    html.Br(),
    dcc.Link('Era Features', href='/eras'),
    html.Br(),
    dcc.Link('Song Features', href='/features'),
    html.Br(),
    dcc.Link('Lyrics', href='/lyrics')
])


@app.callback(
    [Output('page-content', 'children'), Output('prev-page', 'href'), Output('next-page', 'href')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == "/":
        return index, "/lyrics", "/scatter"
    elif pathname == "/scatter":
        return scatter.content, "/", "/genres"
    elif pathname == "/genres":
        return genres.content, "/scatter", "/eras"
    elif pathname == "/eras":
        return eras.content, "/genres", "/features"
    elif pathname == "/features":
        return features.content, "/eras", "/lyrics"
    elif pathname == "/lyrics":
        return lyrics.content, "/features", "/"
    return "404"


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
