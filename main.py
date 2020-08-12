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

def frame_preprocessing(frame):
    '''
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converting from opencv image to PIL image
    img_pil = Image.fromarray(img)

    resize = transforms.Resize((224,224))
    color = transforms.ColorJitter(0.1,0.1,0.1,0.1)
    to_tensor = transforms.ToTensor()
    
    frame_resize = resize(img_pil)
    frame_color = color(frame_resize)
    img_tensor = to_tensor(frame_color)
    img_tensor = img_tensor.unsqueeze(0)
    '''
    device = torch.device('cuda')

    frame = cv2.resize(frame, (224,224))
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = frame.transpose((2,0,1))
    frame = torch.from_numpy(frame).float()
    frame = frame.to(device)
    frame = frame[None, ...]
    return frame

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
    model = Net2()
    model.eval()
    print("Loading Neural Network")
    model.load_state_dict(torch.load('/home/dlinano/Desktop/Autonomous-RC-Car-Milestone-2/Data_Collection/PyTorch_Training/Autonomous_RC_Car_Net2_3.pt')) #Load Model
    model.cuda()
    #model.eval()
    #device = torch.device('cuda')
    #model.to(device)
    print("loaded Neural Network")

    data_transform = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])
    #now = datetime.now()
    #prev_time = now.strftime("%H%M%S%f")
    while True:      
        #Reading from the camera Thread
        frame = camera.read()

        img_tensor = frame_preprocessing(frame)
        #img_pil = Image.fromarray(frame)
        #img_tensor = data_transform(img_pil).unsqueeze(0).cuda()
        
        
        
        
        output = model(img_tensor)
        print("ouput: ",output)
        steering = int(180*output[0,1])
        throttle = int(180*output[0,0])
        


        #cv2.imshow('frame', frame)

        if (throttle > 125):
            throttle = 125
        if (steering > 255):
            steering = 90
        print("Throttle: ", throttle, " Steering: ", steering)
        displayThrottle_Steering(frame, throttle, steering)

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




