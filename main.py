import Controls
import cv2
import numpy as np
import time
import threading
from Camera import Camera_Thread
import i2c
from FPS_Calculate import FPS
import Camera
import multiprocessing as mp

from torchvision import datasets
from torchvision import datasets, transforms
from torch.utils.data.sampler import SubsetRandomSampler
import time
from PIL import Image
import torch

from PyTorch_NeuralNetwork import CNN1

from datetime import datetime

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
    return img_tensor

if __name__ == '__main__':

    #For tuning Region of Interest of camera
    #init_TrackBarVals = [0, 263, 0, 512]
    #Perception_functions.ROI_InitTrackbars(init_TrackBarVals, 640, 480) 

    i2c_break_q = mp.Queue()
    data_q=mp.Queue()
    #display = 1
    
    camera = Camera_Thread().start() #Seperate Thread for streaming video from the camera 
    
    i2c_process = mp.Process(target=i2c.i2c_process, args=(data_q, i2c_break_q))
    i2c_process.start()

    time.sleep(3.0)
    fps = FPS().start() #To determine approximate throughput of camera and program
    frame_cnt = 60
    i = 0
    start_time = (time.time()-1)
    model = CNN1()
    model.eval()
    model.load_state_dict(torch.load('/Data_Collection/PyTorch_Training/Autonomous_RC_Car2.pt')) #Load Model
    device = torch.device('cuda')
    model.to(device)
    
    #now = datetime.now()
    #prev_time = now.strftime("%H%M%S%f")
    while True:      
        #Reading from the camera Thread
        frame = camera.read()

        img_tensor = frame_processing(frame)
        output = model(img_tensor)
        steering = int(180*output[0,1])
        throttle = int(180*output[0,0])

        #Controls Module
        #SteeringCommand = Controls.PID_SteeringControl(start_time, Path_Command, Feedback, sum_hist)
        #ThrottleCommand = Controls.Throttle_Control(SteeringCommand)

        #If not using PID Control
        #SteeringCommand = int((Feedback - Path_Command)/(-1.17))

        #print("PID Steering: ", SteeringCommand, "Raw Steering: ", (Feedback - Path_Command))
        #print("Throttle Command: ", ThrottleCommand)

        #Sending Throttle and Steering Values over i2c to Arduino
        data_q.put([throttle, steering])

        fps.update()
        i += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Main Thread Loops: ", i)
            fps.stop()
            i2c_break_q.put(1)
            time.sleep(2)
            i2c_process.terminate()
            i2c_process.join()
            camera.stop()
            break 


    print("Elapsed Time: ", fps.elapsed())
    print("Approx FPS: ", fps.fps())




