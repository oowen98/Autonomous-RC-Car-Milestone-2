import sys

sys.path.insert(1, '/home/dlinano/Desktop/Autonomous-RC-Car-Milestone-2')

import Camera
import i2c
from datetime import datetime

if __name__ == "__main__":

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")
        ThrottlePWM, SteeringPWM = i2c.readSteeringThrottle()
        print(current_time, " ThrottlePWM: ", ThrottlePWM, "SteeringPWM: ", SteeringPWM)    
