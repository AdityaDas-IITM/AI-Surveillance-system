import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import numpy as np
import os
from flask import Flask,Response
import plotly.graph_objects as go

import flask

#app = dash.Dash(__name__)
app=dash.Dash(__name__,external_stylesheets = [dbc.themes.UNITED])

navbar = dbc.NavbarSimple(
           children=[
            
              dbc.NavItem(dbc.NavLink("Options",href="options")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Start Feed",href="/start-feed"),
                    dbc.DropdownMenuItem("Recent Anamolies",href="/recent-feed"),
                    
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",)

layout_page_1 = html.Div([
    html.H2('Start Feed'),
    
    html.Br(),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/recent-feed"', href='/recent-feed')
])

layout_page_2 = html.Div([
    html.H2('Recent feed'),
    
    html.Div(id='page-2-display-value'),
    html.Br(),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/start-feed"', href='/start-feed')
])
body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("SecurAI"),
                     html.P(
                         """\Do not let any other crime unnoticed"""
                           ),
                           dbc.Button("View details", color="secondary"),
                   ],
                
               ),
              
                     
                ]
            ),
       ],
className="mt-4"
)

page = html.Div(id = 'page-content')
url_bar = dcc.Location(id = 'url', refresh = False)
# "complete" layout
layout=html.Div([url_bar,navbar,page])
app.layout=layout

# Index callbacks
@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == "/start-feed":
        return [layout_page_1]
    elif pathname == "/recent-feed":
        return [layout_page_2]
    else:
        return [body]

# Page 1 callbacks



if __name__ == '__main__':
    app.run_server(debug=True)