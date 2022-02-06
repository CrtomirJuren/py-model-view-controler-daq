"""
THIS IS THE MODEL LAYER

- Main logic on how the hardware should function
- Logic should be here and NOT IN controller=driver
"""

from time import sleep
from src.controller.pftl_daq import Device

class AnalogDaq:
    """ """
    
    def __init__(self, port):
        """ """
        self.port = port
        self.driver = Device(self.port)

    def initialize(self):
        """ """
        # initialize driver
        self.driver.initialize()
        
        # clear outputs
        self.set_voltage(0,0)
        self.set_voltage(1,0)

    def get_voltage(self, channel):
        """ """
        # query ADC value from driver
        voltage_bits = self.driver.get_analog_input(channel)
        # transform ADC -> voltage
        voltage = voltage_bits * 3.3/1023
        
        return voltage

    def set_voltage(self, channel, volts):
        """ """
        # transform voltage -> bits
        voltage_bits = int(volts * 4095/3.3)
        print(voltage_bits)
        # send value to driver 
        self.driver.set_analog_output(channel, voltage_bits)

    def finalize(self):
        """ """
        # clear outputs
        self.set_voltage(0,0)
        self.set_voltage(1,0)

        # finalize driver
        self.driver.finalize()


def blink_test():
    daq = AnalogDaq('COM6')
    daq.initialize()

    # blink led 
    for i in range(5):
        daq.set_voltage(0, 3.3)
        sleep(0.2)
        daq.set_voltage(0, 0)
        sleep(0.2)

    daq.finalize()

if __name__ == '__main__':
    blink_test()