import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import base64
import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory,Response
import cv2
#import dash_auth
import plotly
from PIL import  Image
import numpy as np
from multiprocessing import Process, Queue
from model import C3D, fc
import torch
import torch.nn as nn
import torch.nn.functional as F

server = Flask(__name__)
app=dash.Dash(__name__,external_stylesheets = [dbc.themes.UNITED], suppress_callback_exceptions=True, server=server)

UPLOAD_DIRECTORY = "D:/Github Repos/AI-Surveillance-system/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

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

number_input = html.Div(id='input',
    children = [dbc.Input(type="number",placeholder='Enter Phone Number', min=600000000, max=9999999999)]
    )

output = html.Div(id = 'output')

layout_page_1 = html.Div([html.Br(),output,
    html.H2('Start Feed'),
    html.H3("File Browser"),
    html.H4("Upload"),
        
    html.Div([dcc.Upload(
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
        multiple=False,
        )]),
    html.H1("Live Feed"),
    html.Img(src="/video_feed"),
        #html.H2("File List"),
        #html.Ul(id="file-list"),
        ],
    style={"max-width": "500px"},
)


layout_page_2 = html.Div([
    html.H2('Recent feed'),
    html.H3("File List"),
    html.Ul(id="file-list"),])



@app.callback(Output("output", "children"), Input("input", "value"))
def num(a):
    print("called")
    if a is not None:
        print(a)
        return [html.P(str(a))]
    else:
        return [html.P("Enter a valid number")]

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
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

@app.callback(Output("file-list", "children"), [Input("upload-data", "contents"), Input("upload-data", "filename")])
def update_output(uploaded_file_contents, uploaded_filenames):
    #if (uploaded_filenames is not None) and (uploaded_file_contents is not None):
    print("called")
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


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, self.image = self.video.read()
        _, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tobytes()


def gen(camera):
    inp = []
    #pred_temp = []
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    c3d_model = C3D().to(device)
    model = fc().to(device)
    c3d_model.load_state_dict(torch.load("D:/Hackathons/video surveilance/c3d weights.pickle"))
    model.load_state_dict(torch.load('D:/Github Repos/AI-Surveillance-system/models/model.pth'))
    c3d_model.eval()
    model.eval()
    while True:

        frame = camera.get_frame()
        image = cv2.resize(camera.image, (112,112))
        inp += [image]
        if len(inp) == 16:
            inp = np.array(inp).transpose(3,0,1,2)
            inp = torch.Tensor(np.expand_dims(inp, axis=0)).to(device)
            pred = c3d_model(inp).detach().cpu().numpy()
            pred = torch.Tensor(np.reshape(pred/np.linalg.norm(pred), (-1,4096))).to(device)
            #pred_temp+= [pred]
            #if len(pred_temp) == 5:
                #pred = torch.mean(torch.Tensor(pred_temp),axis = 0, keepdims = False)
                #pred_temp = []
            value = model(pred).detach().cpu().numpy()[0][0]
            print(value)
            inp = []
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@server.route('/video_feed')
def video_feed():
    img = Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    return img




page = html.Div(id = 'page-content')
url_bar = dcc.Location(id = 'url', refresh = False)

app.layout=html.Div([url_bar,navbar,page])


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
    