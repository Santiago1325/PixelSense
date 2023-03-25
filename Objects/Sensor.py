import numpy as np
import cv2
from mss import mss
from abc import ABC, abstractmethod
import time


import magichue


TOKEN = 'eyJhbGciOiJSUzI1NiJ9.eyJhcHBLZXkiOiJaRzAwMSIsImNkcElkIjoiWkcwMDEiLCJjbGllbnRJZCI6Ik1ON1dBMVZZSjdBUFNHTTRNWDg3SENaNkQyMU5EWFAyIiwiZXhwaXJlRGF0ZSI6MTY5Mzc5MDkxMTY3OSwiZ3Vlc3QiOmZhbHNlLCJsb2dpbkRhdGUiOjE2NzgyMzg5MTE2NzksInJlZnJlc2hEYXRlIjoxNjg4NjA2OTExNjc5LCJzZXJ2ZXJDb2RlIjoiVVMiLCJ1aWQiOjE2MzMyMzU2ODAzOTQzMzgzMDYsInVzZXJJZCI6InNhbnRpYWdvajIyMkBnbWFpbC5jb20ifQ.n0GkAldq_xBzOgfnUskmBKWnAlSoujuzJs54WVP8KDpQ6AsJIBnvoqnxohbf-UBTrlwqlNiINT92irboO9e-fKc53dRqz-JQW3_C2FMls_lF5V10qE05fg91wfTKfvCJGdYTyqAKgV6SjCYucpb4O5DflbAlqhrAe49BE2HEw7nbGRnJsx9YMoO0ZZ6RpulF6CLqthz7qBl-0DgtQfTHecD3RJ7COvBl_qigFOvI8EHt83Mzjb77LT7dAlNW27oqC0115HFsW4duUujK4PxJPQhg9jKPY40DzTaiqYakHCZ7CkrJxGlGPScDGSk6Do5A_9CvcaYW7jRZT5LvZD2Caw'
api = magichue.RemoteAPI.login_with_token(TOKEN)
light = api.get_online_bulbs()[0]
light.rgb = (0,255,0)

PoliceLights = magichue.CustomMode(
    mode = magichue.MODE_JUMP,
    speed = 0.85,
    colors= [(255, 0, 0),   (0, 0, 255)],
)

police_pursuit = False




#ToDo
#MaskSensor
#ConvolutionalSensor


class Sensor(ABC):

    @abstractmethod
    def __init__(self):
        ...
                    
    @abstractmethod
    def grab_data(self):
        ...
    
    @abstractmethod
    def trigger(self):
        ...
        

        
class MaskSensor(Sensor):
    """
    Base class of the Sensor. Will recieve the monitor and the area that will screenshot
    with top = 0 and left = 0 being the upper left corner of the screen.
    and width or height being the extension of each dimension
    If only the monitor is provided it will take a full screenshot
    box = (left, top, width, height)
    """   
    
    
    def __init__(self, monitor_num, mask = None, treshold = None, background = np.array([0,0,0]),box=None):
        
        #Screenshot taker
        self.sct = mss()
        
        self.mask = mask.astype(float)
        
        self.treshold = treshold
        
        self.background = background
        
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
                
                self.box = {"left":box[0], "top":box[1], "width":box[2], "height":box[3]}
            
    def grab_data(self):
        img = self.sct.grab(self.box)
        return np.array(img)[...,:3].astype(float)
    
    def trigger(self):
        pw_abs = abs(self.grab_data() - self.mask).astype(np.uint8)
        bool_mask =  (self.mask == self.background).all(axis=2,  keepdims=True).astype(int)
        bool_mask = np.ones(bool_mask.shape) - bool_mask
        mean_sum = np.mean(bool_mask * pw_abs)
        print(mean_sum)
        return mean_sum < self.treshold
    
    
    
#Example
#(left, top, widht, height)
gta_mask = cv2.imread("C:/Users/Santiago/Pictures/gta_stars_mask.png")
s = MaskSensor(1, mask = gta_mask, treshold = 1, box = (1861,9,34,47))

time_check = 3

while True:
    #img = s.grab_data().astype(np.uint8)
    #cv2.imshow('screen', img)
    #cv2.waitKey(1000)
    #cv2.imshow('screen', gta_mask)
    #cv2.waitKey(1000)
    police_pursuit = s.trigger()
    if police_pursuit and light.rgb == (0,255,0):
        light.mode = magichue.RED_BLUE_CROSSFADE
        time.sleep(5)
    elif not police_pursuit and light.mode == magichue.RED_BLUE_CROSSFADE:
        light.rgb = (0,255,0)
        time.sleep(1)
    
    
        
    #cv2.waitKey(2000)


    #if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #cv2.destroyAllWindows()
        #break
    