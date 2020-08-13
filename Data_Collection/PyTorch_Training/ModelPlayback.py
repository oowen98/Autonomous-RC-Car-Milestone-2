import cv2
import numpy as np
import pandas as pd
import torch
import sys

from torchvision import datasets
from torchvision import datasets, transforms
from torch.utils.data.sampler import SubsetRandomSampler
import time
from PIL import Image

import sys

#Choose depending if running on Windows or Jetson Nano
#sys.path.insert(1, 'C:/Users/Owen/Desktop/Projects/Autonomous RC Car/Autonomous-RC-Car-Milestone-2')
sys.path.insert(1, '/home/dlinano/Desktop/Autonomous-RC-Car-Milestone-2/')

sys.path.insert(1, 'C:/Users/Owen/Desktop/Projects/Autonomous RC Car/Autonomous-RC-Car-Milestone-2')

import PyTorch_NeuralNetwork

def frame_processing(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converting from opencv image to PIL image
    img_pil = Image.fromarray(img)

    resize = transforms.Resize((224,224))
    color = transforms.ColorJitter(0.1,0.1,0.1,0.1)
    to_tensor = transforms.ToTensor()
    
    frame_resize = resize(img_pil)
    frame_color = color(frame_resize)
    img_tensor = to_tensor(frame_color)
    img_tensor = img_tensor.unsqueeze(0)

    #img_tensor = img_tensor.to(torch.device('cuda'))
    return img_tensor

def map_value(value, lower_in=0, upper_in=180, lower_out=-100, upper_out=100):
    return ((value - lower_in) * (upper_out - lower_out) // (upper_in - lower_in) + lower_out)
    
def displayThrottle_Steering(frame, throttle, steering):
    
    throttle = map_value(throttle)
    steering = map_value(steering)
    
    #Visualizing Steering output from the PyTorch Neural Network
    cv2.line(frame, (frame.shape[1]//2, 400), (frame.shape[1]//2,500),(255,0,255), 5 ) #Draw Centre of Steering
    cv2.line(frame, ((frame.shape[1]//2) + steering, 400), ((frame.shape[1]//2) + steering, 500), (255,255,0), 5) #Steering from model
    cv2.line(frame, (frame.shape[1]//2,450), ((frame.shape[1]//2) + steering, 450), (255,255,255), 5) #Difference betweeing Steering and centre

    #Visualizing Throttle output from the PyTorch Neural Network
    cv2.line(frame, (525, frame.shape[0]//2),(575, frame.shape[0]//2), (255,0,255), 5)
    cv2.line(frame, (525, (frame.shape[0]//2) - throttle), (575, (frame.shape[0]//2) - throttle), (255,255,0), 5) #Throttle from model
    cv2.line(frame, (550, frame.shape[0]//2), (550, (frame.shape[0]//2 - throttle)), (255,255,255), 5 )

    cv2.imshow('frame', frame)


if __name__ == "__main__":
    model = PyTorch_NeuralNetwork.Net2()
    model.eval()
    model.load_state_dict(torch.load('Autonomous_RC_Car_Net2_5.pt')) #Load Model
    device = torch.device('cuda')
    model.to(device)

<<<<<<< HEAD
    VideoPath = 'C:/Users/Owen/Desktop/Projects/Autonomous RC Car/Autonomous RC Car Milestone 1/Data Collection/SingleLane_July20.mp4'
    VideoPath2 = 'C:/Users/Owen/Desktop/TrackDriving_Aug11.mp4'
    cap = cv2.VideoCapture(VideoPath2)
=======
    VideoPath = 'SingleLane_July20.mp4'

    cap = cv2.VideoCapture(VideoPath)
>>>>>>> 8741cde128c40789563c2d5d397e058f80eaaf09
    frame_cnt = 0

    while True:
        frame_cnt += 1
        
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == 60:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            break
            cap.release()
            cv2.destroyAllWindows()
            frame_cnt = 0
            
            
        success, frame = cap.read()
        if(success == 0):
            print("Failed to open video")
            break

        img_tensor = frame_processing(frame)
        img_tensor = img_tensor.to(device)
        #print("tensor shape: ", img_tensor.shape)
        output = model(img_tensor)
        
        steering = int(180*output[0,1])
        throttle = int(180*output[0,0])
        print("output: ", output)
        print("Throttle, Steering: ", throttle, " ", steering)
        displayThrottle_Steering(frame, throttle,steering)
            
        #cv2.imshow('frame', frame)
        if cv2.waitKey(60) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()