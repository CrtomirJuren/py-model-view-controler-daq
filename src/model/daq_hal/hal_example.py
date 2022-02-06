# main imports
from src import *

# DAQ_NAME = 'AnalogDaq'
DAQ_NAME = 'SimDaq'

if DAQ_NAME == 'AnalogDaq':
    from src.model.daq_hal.daq_analog import AnalogDaq
    daq = AnalogDaq('COM6')

elif DAQ_NAME == 'SimDaq':
    from src.model.daq_hal.daq_sim import SimDaq
    # from daq_sim import SimDaq
    daq = SimDaq('sine')
else:
    raise Exception(f' {DAQ_NAME} module not implemented or found.')
    # here put logging error
    # logging.critical()

daq.initialize()

print(daq.get_device_info())

# blink led 
for i in range(5):
    daq.set_voltage(0, 3.3*V)
    meas_voltage = daq.get_voltage(0)
    time.sleep(0.1)
    logging.debug('{:.3f}'.format(meas_voltage))
    # print(type(daq.get_voltage(0)))
    time.sleep(0.2)

    daq.set_voltage(0, 0*V)
    # daq.get_voltage(0)
    time.sleep(0.2)

daq.finalize()
