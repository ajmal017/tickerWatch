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

    html.P(children=["Enter a ticker here if you can't find it in the dropdown: ", dcc.Input(
        id='input-field',
        value='TSLA',
        debounce=True
    )]),

    dcc.Dropdown(
        id='dropdown',
        value=['TSLA'],
        multi=True,
        options=dropdown_options
    ),

    html.Button(
        'Add plot',
        id='add-plot-button', 
        n_clicks=0,
        style={'display': 'inline-block'},

    ),

    html.H3(id='current-stock'),

    html.Div(id='container', children=[])

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
    Output('container', 'children'), # not read as input when using state
    [Input('add-plot-button', 'n_clicks')], # first value read to input
    [State('container', 'children'), # same property as output, treat as output variable
    State('dropdown', 'value')]
)
def add_component_to_container(n_clicks, children, dropdown_vals):
    print(n_clicks, children, dropdown_vals)
    children.append(
        html.Div(
            style={'width': '23%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
            children=[html.Div(children=ticker, id=ticker) for ticker in dropdown_vals]
        )
    )
    return children


if __name__ == '__main__':
    # open server and host app
    # tell Dash to refresh our browser every time we make a code change
    app.run_server(debug=True)