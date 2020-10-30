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
import numpy as np
from multiprocessing import Process, Queue
from model import C3D, fc
import torch
import torch.nn as nn
import torch.nn.functional as F
from notif import send_vid
import glob
from selenium import webdriver
import time

server = Flask(__name__)
app=dash.Dash(__name__,external_stylesheets = [dbc.themes.UNITED], suppress_callback_exceptions=True, server=server)

UPLOAD_DIRECTORY = "../app_uploaded_files"
cam = None
list_of_videos = [os.path.basename(x) for x in glob.glob('{}*.mp4'.format(UPLOAD_DIRECTORY+'/'))]
static_video_route = '/static/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

navbar = dbc.NavbarSimple(
           children=[
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
    html.H1("Live Feed"),
    html.Img(src="/video_feed"),
        #html.H2("File List"),
        #html.Ul(id="file-list"),
        ],
    style={'margin-left':'25%'},
)


layout_page_2 = html.Div([
    html.H2('Recent feed'),
    html.H3("File List"),
    html.Ul(id="file-list"),
    html.Div([dcc.Dropdown(
        id='video-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_videos],
        value=list_of_videos[0]
    )], style = {'width': '35%'}),
    html.Br(),
    html.Video(id='video', autoPlay=True, loop=True)],
    style={'margin-left':'25%'})

body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("SecurAI"),html.Br(),
                     html.P(
                         """Do not let another crime go unnoticed"""
                           ),html.Br(),html.Br(),html.H1("Every Year 60% of Thefts go unreported or unsolved."),
                           html.H3("\nYou can ensure this not happening again with us"),
                           
                   ],
                
               ),
              
                     
                ],style={'margin-left':'18%'},
            ),
        dbc.Row(
           [
               dbc.Col(
                  [html.Br(),dcc.Input(id="number", type="number", placeholder="Enter your Phone Number", min = 6000000000, max = 9999999999),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                     html.H4("Aditya Das, Aryan Pandey, Joy Jefferson, Nihal John George"),
                     
                     
                           
                   ],
                
               ),
              
                     
                ],style={'margin-left':'15%'},
            ),
        
       ],
className="mt-4"
)

@app.callback(Output("number", 'disabled'), Input("number", 'value'))
def phonenum(num):
    global queue2
    if num is not None:
        queue2.put(str(num))
        return True
    else:
        return False
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
    global queue1
    inp = []
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    c3d_model = C3D().to(device)
    model = fc().to(device)
    c3d_model.load_state_dict(torch.load("../models/c3d weights.pickle"))
    model.load_state_dict(torch.load("../models/model.pth"))
    c3d_model.eval()
    model.eval()
    while True:

        frame = camera.get_frame()
        image = cv2.resize(camera.image, (112,112))
        inp += [image]
        if len(inp) == 16:
            inp1 = np.array(inp).transpose(3,0,1,2)
            inp1 = torch.Tensor(np.expand_dims(inp1, axis=0)).to(device)
            pred = c3d_model(inp1).detach().cpu().numpy()
            pred = torch.Tensor(np.reshape(pred/np.linalg.norm(pred), (-1,4096))).to(device)
            value = model(pred).detach().cpu().numpy()[0][0]
            print(value)
            if value > 0.15:
                queue1.put(inp)
                #send_vid("+919740718396","../app_uploaded_files/output.mp4")
            inp = []
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@server.route('/video_feed')
def video_feed():
    global cam
    img = Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    return img

@app.callback(
    dash.dependencies.Output('video', 'src'),
    [dash.dependencies.Input('video-dropdown', 'value')])
def update_image_src(value):
    return static_video_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<video_path>.mp4'.format(static_video_route))
def serve_video(video_path):
    video_name = '{}.mp4'.format(video_path)
    if video_name not in list_of_videos:
        raise Exception('"{}" is excluded from the allowed static files'.format(video_path))
    return send_from_directory(UPLOAD_DIRECTORY+'/', video_name)

page = html.Div(id = 'page-content')
url_bar = dcc.Location(id = 'url', refresh = False)

app.layout=html.Div([url_bar,navbar,page])


@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    #print(pathname)
    global cam
    if pathname == "/start-feed":
        cam = VideoCamera()
        return [layout_page_1]
    elif pathname == "/recent-feed":
        try:
            cam.__del__()
        except:
            pass
        return [layout_page_2]
    else:
        try:
            cam.__del__()
        except:
            pass
        return [body]
    
        


def send_msgs(queue1, queue2):
    phone_num = queue2.get()
    i=0
    driver = webdriver.Chrome(executable_path='../scripts/chromedriver.exe')
    wapp = 'https://web.whatsapp.com/send?phone='+'+91'+phone_num
    driver.get(wapp)
    time.sleep(15)
    while True:
        inp = queue1.get()
        save = cv2.VideoWriter(f"../app_uploaded_files/output{i}.mp4", -1, 20, (512,512))
        for fr in inp:
            save.write(cv2.resize(fr,(512,512)))
        save.release()
        send_vid(driver, os.path.abspath(f'../app_uploaded_files/output{i}.mp4'))
        i+=1

if __name__ == '__main__':

    queue1 = Queue()
    queue2 = Queue()
    msg_p = Process(target = send_msgs, args=(queue1,queue2))
    msg_p.start()
    #time.sleep(15)
    app.run_server(debug=False)
    msg_p.join()
    