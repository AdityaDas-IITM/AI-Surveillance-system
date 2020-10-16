import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
import pandas as pd
import random
from tensorboardX import SummaryWriter
from model import C3D, fc
import cv2

def makecsv():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    anomaly_path_burg = "D:/Hackathons/video surveilance/archive/Anomaly-Videos-Part-2/Burglary"
    anomaly_path_fight = "D:/Hackathons/video surveilance/archive/Anomaly-Videos-Part-2/Fighting"
    anomaly_burg = os.listdir(anomaly_path_burg)
    anomaly_fight = os.listdir(anomaly_path_fight)
    normal_path = "D:/Hackathons/video surveilance/archive/Testing_Normal_Videos/Testing_Normal_Videos_Anomaly"
    normal = os.listdir(normal_path)
    
    save_anomaly = "D:/Hackathons/video surveilance/archive/Anomaly csv"
    save_normal = "D:/Hackathons/video surveilance/archive/Normal csv"

    c3d_model = C3D().to(device)
    c3d_model.load_state_dict(torch.load("D:/Hackathons/video surveilance/c3d weights.pickle"))
    
    for vid in anomaly_burg:
        cap = cv2.VideoCapture(os.path.join(anomaly_path_burg, vid))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        final = []
        temp = []
        inp = []
        while(cap.isOpened()):
            ret,frame = cap.read()
            if ret == True:
                frame = cv2.resize(frame, (112,112))
                inp += [np.array(frame)] 
                if len(inp) == 16:
                    inp = np.array(inp).transpose(3,0,1,2)
                    inp = torch.Tensor(np.expand_dims(inp, axis=0)).to(device)
                    pred = c3d_model(inp).detach().cpu().numpy()
                    pred = list(pred/np.linalg.norm(pred))
                    temp += pred
                    inp = []

            else:
                break
            
        cap.release()
        seg_length = int(len(temp)//32)
        if seg_length == 0:
            continue
        for i in range(0,32*seg_length, seg_length):
            final += [np.average(temp[i:i+seg_length], axis = 0)]
        final = np.array(final).reshape((32,4096))
        pd.DataFrame(final).to_csv(os.path.join(save_anomaly, vid.split('.')[0] + '.csv'), index = False)
    
    for vid in anomaly_fight:
            cap = cv2.VideoCapture(os.path.join(anomaly_path_fight, vid))
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            final = []
            temp = []
            inp = []
            while(cap.isOpened()):
                ret,frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame, (112,112))
                    inp += [np.array(frame)] 
                    if len(inp) == 16:
                        inp = np.array(inp).transpose(3,0,1,2)
                        inp = torch.Tensor(np.expand_dims(inp, axis=0)).to(device)
                        pred = c3d_model(inp).detach().cpu().numpy()
                        pred = list(pred/np.linalg.norm(pred))
                        temp += pred
                        inp = []

                        
                else:
                    break
            cap.release()
            seg_length = int(len(temp)//32)
            if seg_length == 0:
                continue
            for i in range(0,32*seg_length, seg_length):
                final += [np.average(temp[i:i+seg_length], axis = 0)]

            final = np.array(final).reshape((32,4096))
            pd.DataFrame(final).to_csv(os.path.join(save_anomaly, vid.split('.')[0] + '.csv'), index = False)

    for vid in normal:
            cap = cv2.VideoCapture(os.path.join(normal_path, vid))
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            final = []
            temp = []
            inp = []
            while(cap.isOpened()):
                ret,frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame, (112,112))
                    inp += [np.array(frame)] 
                    if len(inp) == 16:
                        inp = np.array(inp).transpose(3,0,1,2)
                        inp = torch.Tensor(np.expand_dims(inp, axis=0)).to(device)
                        pred = c3d_model(inp).detach().cpu().numpy()
                        pred = list(pred/np.linalg.norm(pred))
                        temp += pred
                        inp = []

                        
                else:
                    break
            cap.release()
            seg_length = int(len(temp)//32)
            if seg_length == 0:
                continue
            for i in range(0,32*seg_length, seg_length):
                final += [np.average(temp[i:i+seg_length], axis = 0)]

            final = np.array(final).reshape((32,4096))
            pd.DataFrame(final).to_csv(os.path.join(save_normal, vid.split('.')[0] + '.csv'), index = False)

def loss(normal, abnormal, lambda1, lambda2):
    MIL = F.relu(1-torch.max(abnormal)+torch.max(normal))
    sparse = torch.sum(abnormal, dim = 1)
    shifted_abnormal = torch.ones(abnormal.size()).to(abnormal.device)
    for i in range(31):
        shifted_abnormal[:,i+1,:] = abnormal[:,i,:]
    abnormal = abnormal[:,1:,:]
    shifted_abnormal = shifted_abnormal[:,1:,:]
    similarity = torch.sum(torch.square(abnormal - shifted_abnormal), dim = 1)
    final_loss = MIL + lambda1*similarity + lambda2*sparse
    final_loss = torch.mean(final_loss, dim = 0)
    return final_loss

def train(iterations, batch_size):
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    model = fc().to(device)
    #model.load_state_dict(torch.load("D:/Hackathons/video surveilance/model.pth"))
    lambda1 = 0.00008
    lambda2 = 0.00008
    lambda3 = 0.01

    anomaly_path = "D:/Hackathons/video surveilance/archive/Anomaly csv"
    normal_path = "D:/Hackathons/video surveilance/archive/Normal csv"

    anomaly = os.listdir(anomaly_path)
    normal = os.listdir(normal_path)
    optim = torch.optim.Adagrad(model.parameters(), lr = 0.001, weight_decay = lambda3)
    loss_prev = 100
    for j in range(iterations):
        normal_files = np.array(normal)[random.sample(range(len(normal)), int(batch_size//2))]
        anomaly_files = np.array(anomaly)[random.sample(range(len(anomaly)), int(batch_size//2))]

        normals = []
        anomalies = []
        for i in range(int(batch_size//2)):
            normals += [torch.Tensor(np.genfromtxt(os.path.join(normal_path, normal_files[i]), delimiter = ','))[1:,:]]
            anomalies += [torch.Tensor(np.genfromtxt(os.path.join(anomaly_path, anomaly_files[i]), delimiter = ','))[1:,:]]
        
        normals = torch.stack(normals, dim = 0).to(device)
        anomalies = torch.stack(anomalies, dim = 0).to(device)

        normal_pred = model(normals)
        anomalies_pred = model(anomalies)

        optim.zero_grad()
        loss_val = loss(normal_pred, anomalies_pred, lambda1, lambda2)
        loss_val.backward()
        optim.step()

        #wandb.log({'Loss':loss_val})
        writer.add_scalar("Loss/loss", loss_val, j)
        if loss_val < loss_prev:
            torch.save(model.state_dict(), "D:/Hackathons/video surveilance/model.pth")
            loss_prev = loss_val
        


if __name__ == '__main__':
    #makecsv()
    writer = SummaryWriter("D:/Hackathons/video surveilance/runs")
    train(iterations = 10000, batch_size = 60)