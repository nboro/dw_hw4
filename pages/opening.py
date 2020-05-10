import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app

title = "We are here for a ride, darling."

content = html.Img(
    src=app.get_asset_url('imgs/freddie.png'),
    className="img-fluid mx-auto d-block"
)

description = html.Div([
    html.H5("Lorem Ipsum", className="text-info"),
    html.P("""
    Illum eius voluptatem nulla mollitia. Dolores doloremque est et atque molestiae dolor. Aut tempore aut quo ratione saepe animi repudiandae illo. Pariatur quia sequi id repudiandae porro dolor. Consequatur sint molestias assumenda rerum qui incidunt consequatur dignissimos.
    """),
    html.P("""
    Necessitatibus ut quibusdam qui illo quae asperiores suscipit. Dicta expedita dolorem dolore. Velit eligendi in minima temporibus commodi cumque. Aliquid adipisci velit repellendus. Non velit excepturi quam necessitatibus nihil reprehenderit non id. Blanditiis ducimus et aut iste veritatis.
    """),
    dcc.Link('Main Scatter', href='/scatter/intro'),
    html.Br(),
    dcc.Link('Genres', href='/genres/intro'),
    html.Br(),
    dcc.Link('Song Features', href='/features'),
    html.Br(),
    dcc.Link('Lyrics', href='/lyrics/intro'),
    html.Br(),
    dcc.Link('Encore', href='/encore')
])
