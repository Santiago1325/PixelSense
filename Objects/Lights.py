from abc import ABC, abstractmethod


class Lights(ABC):

    @abstractmethod
    def __init__(self):
        ...
                    
    @abstractmethod
    def connect(self):
        ...
    
    @abstractmethod
    def set_rgb(self):
        ...
    
    @abstractmethod
    def set_hexa(self):
        ...
        
    @abstractmethod
    def set_sequence(self):
        ...
        
    @abstractmethod
    def turn_on(self):
        ...
        
    @abstractmethod
    def turn_off(self):
        ...
        
