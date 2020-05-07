from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from app import app
from pages import scatter, genre_analysis, features, lyrics

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[
        dbc.Row(
            [
                dbc.Col(html.H1('Data Visualization - Top 2000 Group 3'),className="text-center"),
            ]
        ),
    ]),
    html.Div(id='page-content'),
])

index = html.Div([
    dcc.Link('Main Scatter', href='/scatter'),
    html.Br(),
    # dcc.Link('Genres', href='/genres'),
    # html.Br(),
    dcc.Link('Genres', href='/genres'),
    html.Br(),
    # dcc.Link('Era Features', href='/eras'),
    # html.Br(),
    dcc.Link('Song Features', href='/features'),
    html.Br(),
    dcc.Link('Lyrics', href='/lyrics')
])


@app.callback(
    [Output('page-content', 'children')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == "/":
        return index
    elif pathname == "/scatter":
        return scatter.content
    # elif pathname == "/genres":
    #     return genres.content, "/scatter", "/eras"
    elif pathname == "/genres":
        return genre_analysis.content
    # elif pathname == "/eras":
    #     return eras.content, "/genres", "/features"
    elif pathname == "/features":
        return features.content
    elif pathname == "/lyrics":
        return lyrics.content
    return "404"


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
