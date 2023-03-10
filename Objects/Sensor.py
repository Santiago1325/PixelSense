import numpy as np
import cv2
from mss import mss
from PIL import Image, ImageGrab

class Sensor:
# Base class of the Sensor. Will recieve the monitor and the area that will screenshot
# with top = 0 and left = 0 being the upper left corner of the screen.
# Leave width or height as full to use the full widht or height of the screen
# If only the monitor is provided it will take a full screenshot
    def __init__(self, monitor_num, top = 0, left = 0, width = "full", height = "full"):
        
        #Screenshot taker
        self.sct = mss()
        
        #Verifying the number of monitors
        if monitor_num > len(self.sct.monitors) - 1:
            raise Exception("Number of monitor exceeds the actual monitors")
        
        self.monitor = self.sct.monitors[monitor_num]
        print(self.monitor)
        
        #Checking default arguments
        if width == "full":
            width = self.monitor["width"]
        if height == "full":
            height = self.monitor["height"]

        #Verifying that nor width or height exceed the monitor dimensions
        if width + left > self.monitor["width"] or height + top > self.monitor["height"] or left >= self.monitor["width"] or top >= self.monitor["height"]:
            raise Exception("Arguments exceed the dimensions of the monitor")
        
        self.bbox = {"top": self.monitor["top"] + top, "left": self.monitor["left"] + left, "width": width, "height": height}
        print(self.bbox)
        
    #Take screenshot
    def grab_img(self):
        img = self.sct.grab(self.bbox)
        return np.array(img)
        

#Example
s = Sensor(2,0,1079)

while True:
    img = s.grab_img()
    cv2.imshow('screen', img)
 

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    