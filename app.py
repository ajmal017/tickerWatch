# Imports & Dash app set-up
import sys
sys.path.append('src/')
import pandas as pd
import math
import yfinance_helpers

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
master_df = yfinance_helpers.get_master_stock_data()
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
dropdown_options = []
for (co, ticker) in zip(company_names, master_df.columns):
    option = {'label': co, 'value': ticker}
    dropdown_options.append(option)

fig = go.Figure()

# Layout
app.layout = html.Div(children=[
    html.H1('Stock Tickers'),

    html.H3(id='current-stock'),

    dcc.Graph(
        id='stock-plot',
        figure=fig
        ),

    dcc.Dropdown(
        id='dropdown',
        options = dropdown_options,
        value='MSFT'
    )
])

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
    fig = go.Figure()
    fig.add_trace(go.Line(
        x=master_df.index, 
        y=master_df[prop], 
        name=prop
        ))
    return fig

if __name__ == '__main__':
    # open server and host app
    # tell Dash to refresh our browser every time we make a code change
    app.run_server(debug=True)