import sys

sys.path.insert(1, '/home/dlinano/Desktop/Autonomous-RC-Car-Milestone-2')

import Camera
import i2c
import cv2
import time
import Controls
from datetime import datetime
import os
from uuid import uuid1
import csv

if __name__ == "__main__":

    DataName = "Aug9_DataCollection"
    os.mkdir(DataName)
    os.chdir(DataName)

    camera = Camera.Camera_Thread().start()
    time.sleep(3)
    i = 0
    j = 0

    #Writing the Headers for the .csv file
    with open(DataName+".csv", 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["time","JPG Name","Index", "Throttle_PWM" , "Steering_PWM"])

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")
        
        frame = camera.read()
        cv2.imshow('frame', frame)

        if (i == 30): #Capture 5 samples per second
            j += 1
            ThrottlePWM, SteeringPWM = i2c.readSteeringThrottle()
            ThrottlePWM = Controls.map_value(ThrottlePWM, lower_in = 992, upper_in = 1996)
            SteeringPWM = Controls.map_value(SteeringPWM, lower_in = 940, upper_in = 1968)
            print(current_time, " ThrottlePWM: ", ThrottlePWM, "SteeringPWM: ", SteeringPWM)
            image_name = DataName + "_" + str(j) + ".jpg"
            cv2.imwrite(imange_name, frame)

            #Writing the data to the csv file
            with open(DataName+".csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([current_time,image_name, j, ThrottlePWM, SteeringPWM])

            i = 0    
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera.stop()
            break

        i += 1
        
