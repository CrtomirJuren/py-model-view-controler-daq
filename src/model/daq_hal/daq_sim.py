""" DAQ class to simulate data

"""
# main imports
from src import *

# uniform gives you a floating-point value
from random import uniform

# local imports
# from daq_base import BaseDaq
from src.model.daq_hal.daq_base import BaseDaq # import parent class to override methods

logger = logging.getLogger(__name__)

#TODO Rename to DAQSimulated
class SimDaq(BaseDaq):
    """ """
    
    def __init__(self, port):
        """ """
        self.angle = 0

    def initialize(self):
        """ """
        pass

    def get_device_info(self):
        self.idn = "Simulated DAQ Device"
        return self.idn

    def get_voltage(self, channel):
        """ """
        # rand_noise = uniform(0, 0.01)
        rand_noise = uniform(0, 3.3)
        rand_noise *= V
        return rand_noise

    def set_voltage(self, channel, volts):
        """ """
        # convert value to magintude in volt
        value_volts = volts.m_as('V')

        # transform voltage -> bits
        voltage_bits = round(value_volts * 4095/3.3)

        # send value to display
        print(f'set_voltage ch:{channel} ADC:{voltage_bits}')

    def finalize(self):
        """ """
        pass

    def __str__(self) -> str:
        return "SimDaq"

if __name__ == '__main__':
    daq = SimDaq('sine')
    daq.initialize()
    logging.debug(daq.get_device_info())
    daq.set_voltage(0, 3.3*V)
    daq.finalize()