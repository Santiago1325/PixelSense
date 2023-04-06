import numpy as np
import cv2
from mss import mss
from abc import ABC, abstractmethod

class Sensor(ABC):
    """
    Base abstract class for all sensors
    """

    @abstractmethod
    def __init__(self):
        """
        Init method
        """

                  
    @abstractmethod
    def grab_data(self):
        """
        Method to grab data from the sensor
        """  
    
    @abstractmethod
    def trigger(self):
        """
        Method to trigger the sensor given a certain condition
        """

        

        
class MaskSensor(Sensor):
    """
    Class representing a Mask Sensor
    
    This sensor uses a mask to do a little of image processing to determine
    if the region that is being watched by the sensor contains a certain shape
    given by the mask. If it does the sensor will be triggered
    """

    def __init__(self, monitor_num, mask = None, treshold = None, background = np.array([0,0,0]),box=None):
        """Init method of mask sensor

        Args:
            monitor_num (int): Number of monitor to capture
            mask (Numpy array, optional): Mask that will be used for detection. Defaults to None.
            treshold (float, optional): Treshold that will be used to trigger the sensor. Defaults to None.
            background (Numpy array, optional): Color of the background of the mask. Defaults to np.array([0,0,0]).
            box (tuple, optional): Region of the screen that wiil be captured. Defaults to None.

        Raises:
            Exception: Happens when the number given exceeds the number of available monitors
            Exception: Occurs when the Box argument is not a tuple
            Exception: Raises when the Box argument has more than 4 elements
            Exception: Happens when or more of the given dimensions exceed the monitor dimensions
            Exception: Happens if mask and region dimensions are differents
        """

        self.sct = mss()
        self.mask = mask.astype(float)
        self.treshold = treshold
        self.background = background
        
        if monitor_num > len(self.sct.monitors) - 1:
            raise Exception("Number of monitor exceeds the actual monitors")
        
        self.monitor = self.sct.monitors[monitor_num]
        
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
                
                self.box = {"left":box[0] + self.monitor["left"], "top":box[1] + self.monitor["top"], "width":box[2], "height":box[3]}
        
        if self.mask.shape[0] != self.box["height"] or self.mask.shape[1] != self.box["width"]:
            raise Exception("Mask and region dimensions must be the same")
         
    def grab_data(self):
        """Tells the sensor to take a screenshot of the actual region of the screen

        Returns:
            Numpy array: 3D array containing the info of the image. The last channel is dropped on the return since the alpha channel is not needed
        """
        img = self.sct.grab(self.box)
        return np.array(img)[...,:3].astype(float)
    
    def trigger(self):
        """Determines wether the sensor is triggered or not

        Returns:
            bool: If the result of the operations between the screnshot an the mask is below the trigger treshold
        """
        pw_abs = abs(self.grab_data() - self.mask).astype(np.uint8)
        bool_mask =  (self.mask == self.background).all(axis=2,  keepdims=True).astype(int)
        bool_mask = np.ones(bool_mask.shape) - bool_mask
        mean_sum = np.mean(bool_mask * pw_abs)
        return mean_sum < self.treshold
    