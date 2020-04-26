import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from view_features import layout_features as features
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
server = app.server

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/hw4/features':
         return features
    # elif pathname == '/apps/app2':
    #      return layout2
    else:
        return 'This how now the first page'

if __name__ == '__main__':
    app.run_server(debug=True, port=80)