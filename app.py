import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from yahoo import cdf, get_dates

EPSILON = 1e-3
app = dash.Dash()

app.layout = html.Div([
    dcc.Input(
        id="ticker-input",
        type="text",
        placeholder="Ticker Symbol",
    ),
    dcc.Dropdown(
        id='date-dropdown',
        options=[{'label': d, 'value': d} for d in get_dates("AAPL")],
        value=get_dates("AAPL")[0]
    ),

    html.Button('Get Distribution', id='button'),
    dcc.Graph('probability-dist')
])

@app.callback(Output('date-dropdown', 'options'),
              [Input('ticker-input', 'value')])
def update_dropdown(ticker):
    dates = get_dates(ticker)
    options = [{'label': i, 'value': i} for i in dates]
    return options


@app.callback(Output('probability-dist', 'figure'),
              [Input('button', 'n_clicks')],
              state=[State('date-dropdown', 'value'),
                     State('ticker-input', 'value')]
              )
def update(n_clicks, date, ticker):
    if date is None:
        return None
    data = cdf(ticker, date)
    print(data)
    widths = data['range_start'].diff().tolist()
    widths[0] = widths[1]
    data = [go.Bar(x=data['range_start'], y=data['prob']/np.array(widths), width=widths)]
    fig = go.Figure(data=data)
    return fig


if __name__ == '__main__':
    app.run_server()
