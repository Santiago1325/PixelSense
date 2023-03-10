import numpy as np
import cv2
from mss import mss
from PIL import Image, ImageGrab

class Sensor:
# Base class of the Sensor. Will recieve the monitor and the area that will screenshot
# with top = 0 and left = 0 being the upper left corner of the screen.
# Leave width or height as full to use the full widht or height of the screen
# If only the monitor is provided it will take a full screenshot
#(left, top, width, height)


    def __init__(self, monitor_num, box = None):
        
        #Screenshot taker
        self.sct = mss()
        
        #Verifying the number of monitors
        if monitor_num > len(self.sct.monitors) - 1:
            raise Exception("Number of monitor exceeds the actual monitors")
        
        self.monitor = self.sct.monitors[monitor_num]
        print(self.monitor)
        
        if not box:
            self.box = self.monitor
        else:
            if type(box) != tuple:
                raise Exception("Box must be a tuple")
            elif len(box) > 4 or len(box) < 4:
                raise Exception("Tuple len must have 4 elements")    
            else:
                if box[1] >= self.monitor["height"] or box[0] >= self.monitor["width"] or box[0] + box[2] > self.monitor["width"] or  box[1] + box[3] > self.monitor["height"]:
                    raise Exception("One or more of the given dimensions exceed the monitor dimensions")
                if box[0] > box[2] or box[1] > box[3]:
                    raise Exception("Dimensions don't match")
                self.box = {"left":box[0], "top":box[1], "width":box[2], "height":box[3]}
            
        
    #Take screenshot
    def grab_img(self):
        img = self.sct.grab(self.box)
        return np.array(img)
        

#Example
s = Sensor(1, (0,0,1920,500))

while True:
    img = s.grab_img()
    cv2.imshow('screen', img)
 

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    