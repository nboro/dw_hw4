import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from view_features import layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/hw4/features':
         return layout
    # elif pathname == '/apps/app2':
    #      return layout2
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, port=80)