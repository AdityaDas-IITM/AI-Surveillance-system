#!/usr/bin/env python
# coding: utf-8

# In[76]:


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import numpy as np
import os
from flask import Flask,Response
import plotly.graph_objects as go


# In[68]:


server=Flask(__name__)
app=dash.Dash(__name__)
#if __name__ == '__main__':
    #app.run_server(debug=True)


#


children = [
    html.H2('securAI'),
    html.P('''Never let another crime unnoticed!'''),
    html.P('''Pick an option from the dropdown below.''')
]


# In[61]:


def Navbar():
    navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Options", href="/start-feed")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Start Feed"),
                    dbc.DropdownMenuItem("Recent Anamolies"),
                    
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top")
    return navbar


# In[73]:


body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("securAI"),
                     html.P(
                         """Never let another crime left unnoticed
                               """
                           ),
                           dbc.Button("View details", color="secondary"),
                   ],
                  md=4,
               ),
              
                ]
            )
       ],
className="mt-4",
)


# In[74]:


nav=Navbar()
def Homepage():
    layout = html.Div([
    nav,body
    ])
    return layout




header = html.H3(
    'Drag and Drop the clippings or Start Live Feed'
)
body= #define the body the start feed page





# In[88]:


def App():
    layout = html.Div([header,
        nav,
        body,
        ])
    return layout

app.config.suppress_callback_exceptions = True

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/start-feed':
        return App()
    else:
        return Homepage()


# In[91]:


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




