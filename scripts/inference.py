from multiprocessing import Process, Queue
from model import C3D, fc
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np

def display(queue1, queue2):
    while True:
        frames = queue1.get()
        value = queue2.get()
        if value == -1:
            break
        for frame in frames:
            frame = cv2.resize(frame, (512,512))
            cv2.imshow("Video", frame)
            cv2.waitKey(25)
        #print(value)
        if value > 0.2:
            print("Alert")
    cv2.destroyAllWindows()


def inference(queue1, queue2):
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    c3d_model = C3D().to(device)
    model = fc().to(device)
    c3d_model.load_state_dict(torch.load("../models/c3d weights.pickle"))
    model.load_state_dict(torch.load('../models/model.pth'))
    c3d_model.eval()
    model.eval()
    
    inp = []
    cap = cv2.VideoCapture("../Burglary Video.mp4")
    while(cap.isOpened()):
        ret,frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, (112,112))
            inp += [frame] 
            if len(inp) == 16:
                inp1 = np.array(inp).transpose(3,0,1,2)
                inp1 = torch.Tensor(np.expand_dims(inp1, axis=0)).to(device)
                pred = c3d_model(inp1).detach().cpu().numpy()
                pred = torch.Tensor(np.reshape(pred/np.linalg.norm(pred), (-1,4096))).to(device)
                value = model(pred).detach().cpu().numpy()[0][0]
                queue1.put(inp)
                queue2.put(value)
                inp = []
                
        
        else:
            queue1.put(-1)
            queue2.put(-1)
            break
    cap.release()

if __name__ == '__main__':
    
    queue1 = Queue()
    queue2 = Queue()
    display_p = Process(target=display, args=(queue1,queue2))
    display_p.start()
    inference(queue1, queue2)
    display_p.join()
    print('done')
    
