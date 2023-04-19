import numpy as np
import cv2
from mss import mss
from abc import ABC, abstractmethod
from pydantic import BaseModel

class Box(BaseModel):
    """Pydantic base class for a Box object that defines the region
    that a sensor will look at

    Args:
        BaseModel (_type_): _description_
    """
    left: int
    top: int
    width : int
    height: int


class Sensor(ABC):
    """
    Base abstract class for all sensors
    """
    
    @abstractmethod
    def trigger(self) -> bool:
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

    def __init__(self, monitor_num: int, mask: np.array, treshold: float, box: Box =None ,background: np.array = np.array([0,0,0])):
        """Init method of mask sensor

        Args:
            monitor_num (int): Number of monitor to capture
            mask (Numpy array): Mask that will be used for detection.
            treshold (float): Treshold that will be used to trigger the sensor. 
            background (Numpy array, optional): Color of the background of the mask. Defaults to np.array([0,0,0]).
            box (Box, optional): Region of the screen that wiil be captured. Defaults to None.

        Raises:
            Exception: Happens when the number given exceeds the number of available monitors
            Exception: Occurs when the Box argument is not a Box object
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
            if not isinstance(box, Box):
                raise Exception("Use Pydantic class Box")   
            else:
                if box.height >= self.monitor["height"] or box.width >= self.monitor["width"] or box.left + box.width > self.monitor["width"] or box.top + box.height > self.monitor["height"]:
                    raise Exception("One or more of the given dimensions exceed the monitor dimensions")
                
                self.box = {"left":box.left + self.monitor["left"], "top":box.top + self.monitor["top"], "width":box.width, "height":box.height}
        
        if self.mask.shape[0] != self.box["height"] or self.mask.shape[1] != self.box["width"]:
            raise Exception("Mask and region dimensions must be the same")
         
    def __grab_data(self) -> np.array :
        """Tells the sensor to take a screenshot of the actual region of the screen

        Returns:
            Numpy array: 3D array containing the info of the image. The last channel is dropped on the return since the alpha channel is not needed
        """
        img = self.sct.grab(self.box)
        return np.array(img)[...,:3].astype(float)
    
    def trigger(self) -> bool:
        """Determines wether the sensor is triggered or not

        Returns:
            bool: If the result of the operations between the screnshot an the mask is below the trigger treshold
        """
        pw_abs = abs(self.__grab_data() - self.mask).astype(np.uint8)
        bool_mask =  (self.mask == self.background).all(axis=2,  keepdims=True).astype(int)
        bool_mask = np.ones(bool_mask.shape) - bool_mask
        mean_sum = np.mean(bool_mask * pw_abs)
        return mean_sum < self.treshold
    