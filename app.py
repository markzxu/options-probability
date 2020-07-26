import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

EPSILON = 1e-3
app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/' +
    'gdp-life-exp-2007.csv')


def get_dates():
    return ['2003-02-19', '2003-02-20']


def get_distribution(date, ticker):
    return np.histogram(np.random.normal(0, 1, 1000), bins=100, normed=True)


app.layout = html.Div([
    dcc.Dropdown(
        id='date-dropdown',
        options=[{'label': d, 'value': d} for d in get_dates()],
        value=get_dates()[0]
    ),
    dcc.Input(
        id="ticker-input",
        type="text",
        placeholder="Ticker Symbol",
    ),
    html.Button('Get Distribution', id='button'),
    dcc.Graph('probability-dist')
])


@app.callback(Output('probability-dist', 'figure'),
              [Input('button', 'n_clicks')],
              state=[State('date-dropdown', 'value'),
                     State('ticker-input', 'value')]
              )
def update(n_clicks, date, ticker):
    values, bins = get_distribution(date, ticker)
    data = [go.Bar(x=bins, y=values, width=bins[1]-bins[0]+EPSILON)]
    fig = go.Figure(data=data)
    return fig


if __name__ == '__main__':
    app.run_server()
