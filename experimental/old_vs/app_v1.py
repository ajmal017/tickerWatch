# Imports & Dash app set-up
import sys
sys.path.append('src/')
import pandas as pd
import math
from yfinance_helpers import *
import yfinance

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

import plotly as pt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create some stuff to be displayed
master_ticker_list = get_ticker_list()

dropdown_options = []
for ticker in master_ticker_list:
    option = {'label': ticker, 'value': ticker}
    dropdown_options.append(option)

fig1 = go.Figure()
fig2 = go.Figure()

# Layout
layout_children = [
    html.H1('Stock Tickers'),

    dcc.Input(
        id='input-field',
        value='MSFT',
        debounce=True
    ),

    dcc.Dropdown(
        id='dropdown',
        options=dropdown_options,
        multi=True
    ),

    html.H3(id='current-stock'),

    dcc.Graph(
        id='stock-plot',
        figure=fig2
    )

]
app.layout = html.Div(children=layout_children)

@app.callback(
    Output('dropdown', 'options'),
    [Input('input-field', 'value')]
)
def update_dropdown(prop):
    if prop not in dropdown_options:
        dropdown_options.append({'label':prop, 'value':prop})
    return dropdown_options


@app.callback(
    Output('current-stock', 'children'),
    [Input('dropdown', 'value')]
)
def update_small_header(prop):
    return f'{prop}'

@app.callback(
    Output('stock-plot', 'figure'), 
    [Input('dropdown', 'value')]
)
def update_graph(prop):
    print(prop)
    if prop:
        fig = make_subplots(rows=len(prop), cols=1)
        r = 1
        for p in prop:
            df = get_stock_data(p)
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df.Close, 
                name=p,
                mode='lines'
                ), row=r, col=1)
            r += 1
        return fig
    # else:
    #     df = get_stock_data(prop)
    #     fig.add_trace(go.Scatter(
    #         x=df.index, 
    #         y=df.Close, 
    #         name=prop,
    #         mode='lines'
    #     ), row=1, col=1)

    else:
        fig = go.Figure()
        return fig

if __name__ == '__main__':
    # open server and host app
    # tell Dash to refresh our browser every time we make a code change
    app.run_server(debug=True)