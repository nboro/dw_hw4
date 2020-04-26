from dash.dependencies import Input, Output
from app import app
from data import songs_bill_melt

@app.callback(
    Output('song-feature-99', 'figure'),
    [Input('oldest-first', 'value')])
def update_graph99(oldest_first_value):

    # years = list(songs_bill_melt.bill_year.unique())
    traces = []
    mean_df = songs_bill_melt.groupby(['old','bill_year'])[oldest_first_value].mean().reset_index()

    traces.append(dict(
        x=mean_df[mean_df['old']]['bill_year'],
        y=mean_df[mean_df['old']][oldest_first_value],
        # text=dfy_by_title_year['title_year'],
        mode='lines',
        marker={
            'size': 15,
            'opacity':0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name= 'Songs before 2000'
    ))
    traces.append(dict(
        x=mean_df[~mean_df['old']]['bill_year'],
        y=mean_df[~mean_df['old']][oldest_first_value],
        # text=dfy_by_title_year['title_year'],
        mode='lines',
        marker={
            'size': 15,
            'opacity':0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name='Songs after 2000'
    ))
    return {
        'data': traces,
        'layout': dict(
            title = 'The mean of song features throughout the years',
            xaxis={'title': 'Years'},
            yaxis={'title': 'Mean '+oldest_first_value,'range': [0.0, 1.0]},
            margin={'l': 180, 'b': 40, 't': 50, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
        )
    }