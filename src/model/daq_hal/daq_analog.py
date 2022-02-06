"""
Child of daq_base abstract class

- Main logic on how the hardware should function
- Logic should be here and NOT IN controller=driver

Import requirements, done in main application __init__.py
# import pint
# ur = pint.UnitRegistry()
# V = ur('V')
# mV = ur('mV')
"""

# project packages, modules
from pint import UnitRegistry
from src import * # main application import
from src.controller.pftl_daq import Device # import device driver

# local file
# from daq_base import BaseDaq # import parent class to override methods
from src.model.daq_hal.daq_base import BaseDaq # import parent class to override methods
# C:\Users\crtom\Documents\python\py-model-view-controler-daq\src\model\daq_hal\daq_base.py
# child of base logger, src/__init__.py
logger = logging.getLogger(__name__)
# logger.debug('daq_analog started')

class AnalogDaq(BaseDaq):
    """ """
    
    def __init__(self, port):
        """ """
        self.port = port
        self.driver = Device(self.port)

    def initialize(self) -> None:
        """ """
        # initialize driver
        self.driver.initialize()
        
        # clear outputs
        self.set_voltage(0, 0*V)
        self.set_voltage(1, 0*V)

    def get_device_info(self)-> str:
        self.idn = self.driver.idn()
        return self.idn

    def get_voltage(self, channel:int):
        """ """
        # query ADC value from driver
        voltage_bits = self.driver.get_analog_input(channel)
        # transform ADC -> voltage
        voltage = voltage_bits * 3.3*V/1023

        return voltage

    def set_voltage(self, channel:int, volts: pint.UnitRegistry()):
        """ """
        # convert value to magintude in volt
        value_volts = volts.m_as('V')

        # transform voltage -> bits
        voltage_bits = round(value_volts * 4095/3.3)

        # send value to driver 
        self.driver.set_analog_output(channel, voltage_bits)

    def finalize(self):
        """ """
        # clear outputs
        self.set_voltage(0, 0*V)
        self.set_voltage(1, 0*V)

        # finalize driver
        self.driver.finalize()

    def __str__(self) -> str:
        return "AnalogDaq"

def example_connect():
    daq = AnalogDaq('COM6')
    daq.initialize()
    print(daq.get_device_info())
    daq.finalize()

def example_blink():
    daq = AnalogDaq('COM6')
    daq.initialize()

    # blink led 
    for i in range(5):
        daq.set_voltage(0, ur('3300mV'))
        meas_voltage = daq.get_voltage(0)
        time.sleep(0.1)
        print('{:.3f}'.format(meas_voltage))
        # print(type(daq.get_voltage(0)))
        time.sleep(0.2)

        daq.set_voltage(0, ur('0V'))
        # daq.get_voltage(0)
        time.sleep(0.2)

    daq.finalize()

if __name__ == '__main__':
    # example_connect()
    example_blink()