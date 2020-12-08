# Imports & Dash app set-up
import sys
sys.path.append('src/')
import pandas as pd
import math
from yfinance_helpers import *

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
master_df = get_master_stock_data()
company_names = [
    'Google',
    'Apple', 
    'Amazon', 
    'Facebook',
    'Netflix',
    'Microsoft',
    'Spotify',
    'Tesla'
]
company_tickers = []
dropdown_options = []
for ticker in company_names:
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
        multiple=True,
        debounce=True
    ),

    html.H3(id='current-stock'),

    dcc.Graph(
        id='stock-plot',
        figure=fig2
    )

]
app.layout = html.Div(children=layout_children)


@app.callback(
    Output('current-stock', 'children'),
    [Input('input-field', 'value')]
)
def update_small_header(prop):
    
    print(prop)
    return f'{prop}'

@app.callback(
    Output('stock-plot', 'figure'), 
    [Input('input-field', 'value')]
)
def update_graph(prop):
    print(prop)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=master_df.index, 
        y=master_df[prop], 
        name=prop,
        mode='lines'
        ))
    return fig

if __name__ == '__main__':
    # open server and host app
    # tell Dash to refresh our browser every time we make a code change
    app.run_server(debug=True)