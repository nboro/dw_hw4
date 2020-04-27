from dash import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = 'HW4 Data Visualization Group3 | Top 2000 Dataset'
app.config.suppress_callback_exceptions = True
