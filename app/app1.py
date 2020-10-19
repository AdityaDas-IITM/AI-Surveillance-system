import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory

import os
from flask import Flask,Response
UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


server = Flask(__name__)


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
          brand_href="/",
          sticky="top",)

layout_page_1 = html.Div([
    html.H2('Start Feed'),

    html.H3("File Browser"),
        html.H4("Upload"),
        
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "300px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        )
        #html.H2("File List"),
        #html.Ul(id="file-list"),
    
    
   
],
    style={"max-width": "500px"},
)

layout_page_2 = html.Div([
    html.H2('Recent feed'),
    html.H3("File List"),
    html.Ul(id="file-list"),


    
    
    
])
def save_file(name, content):
    
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

suppress_callback_exceptions=True
@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]
body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("SecurAI"),
                     html.P(
                         """Do not let another crime go unnoticed"""
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
app.layout=html.Div([url_bar,navbar,page,])

suppress_callback_exceptions=True
# Index callbacks
@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    #print(pathname)
    if pathname == "/start-feed":
        return [layout_page_1]
    elif pathname == "/recent-feed":
        return [layout_page_2]
    else:
        return [body]





if __name__ == '__main__':
    app.run_server(debug=True)