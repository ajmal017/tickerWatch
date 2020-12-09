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
    html.H1('TickerWatch'),

    html.H6('Look up and compare historic closes for stocks on your watch list'),

    html.Div(
        style={'width': '39%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'margin':'4.5%'},
        children=[
            html.Div(children=[
                html.P('Lookup symbol by company name: '),
                dcc.Input(
                    id='lookup-symbol-input-field',
                    debounce=True
                ),
                html.Button('Lookup Symbol')
            ])]
    ),

    html.Div(
        style={'width': '39%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'margin':'4.5%'},
        children=[
            html.Div(children=[
                html.P('Enter a ticker here if you can\'t find it in the dropdown: '), 
                dcc.Input(
                    id='add-ticker-input-field',
                debounce=True),
                html.Button(
                    'Add Ticker',
                    id='add-ticker-button',
                    n_clicks=0,
                    style={'display': 'inline-block'}
            )])
        ]
    ),
    
    # html.Div(children=[
    #             html.P('Enter a ticker here if you can\'t find it in the dropdown: '), 
    #             dcc.Input(
    #                 id='add-ticker-input-field',
    #             debounce=True),
    #         html.Button(
    #             'Add Ticker',
    #             id='add-ticker-button',
    #             n_clicks=0,
    #             style={'display': 'inline-block'}
    #         )]
    # ),
        

    html.P('Select tickers from the drop down and press "SHOW PLOTS" to get trends'),

    dcc.Dropdown(
        id='dropdown',
        value=['TSLA'],
        multi=True,
        options=dropdown_options
    ),

    html.Button(
        'Show Plots',
        id='add-plot-button', 
        n_clicks=0,
        style={'display': 'inline-block'}
    ),

    html.H3(id='current-stock'),

    html.Div(id='container', children=[])

]
app.layout = html.Div(children=layout_children)


@app.callback(
    Output('dropdown', 'options'),
    [Input('add-ticker-button', 'n_clicks')],
    [State('dropdown', 'options'),
    State('add-ticker-input-field', 'value')]
)
def update_dropdown(n_clicks, options, value):
    if value:
        if {'label':value, 'value':value} not in options:
            options.append({'label':value, 'value':value})
        return options
    else:
        return options


current_div_ids = []
@app.callback(
    Output('container', 'children'), # not read as input when using state
    [Input('add-plot-button', 'n_clicks')], # first value read to input
    [State('container', 'children'), # same property as output, treat as output variable
    State('dropdown', 'value')]
)
def update_container(n_clicks, children, dropdown_vals):
    print(n_clicks, children, dropdown_vals)
    children = []
    for ticker in dropdown_vals:
        df = get_stock_data(ticker)
        current_div_ids.append(f'{ticker}-div')
        fig = px.line(df, x=df.index, y='Close', title=ticker)
        children.append(
            html.Div(
                id=f'{ticker}-div',
                style={'width': '39%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'margin':'4.5%'},
                children=[
                    dcc.Graph(
                        id=f'{ticker}-graph',
                        figure=fig
                    )
                ]
            )
        )
    return children



if __name__ == '__main__':
    # open server and host app
    # tell Dash to refresh our browser every time we make a code change
    app.run_server(debug=True)