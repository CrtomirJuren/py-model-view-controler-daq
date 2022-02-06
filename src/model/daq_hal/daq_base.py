""" Parent=Base class for all DAQ hardware

ABC (Abstract - Base - Class)
API (Application programming interface)
HAL (hardware abstraction layer)

- Parent=Base Class defines API, how all the similar DAQ classes should function
"""
from src import *

from abc import ABC, abstractmethod
logger = logging.getLogger(__name__)
# from time import sleep

class BaseDaq(ABC):
    """ """
    
    def __init__(self, port):
        """ """
        pass

    @abstractmethod
    def initialize(self):
        """ """
        pass

    @abstractmethod
    def get_device_info(self):
        """ """
        pass

    @abstractmethod
    def get_voltage(self, channel):
        """ """
        return None

    @abstractmethod
    def set_voltage(self, channel, volts):
        """ """
        pass

    @abstractmethod
    def finalize(self):
        """ """
        pass

