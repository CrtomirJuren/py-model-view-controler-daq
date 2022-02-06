# import visa # dont use module like this
from time import sleep
import pyvisa as visa

rm = visa.ResourceManager()
resources = list(rm.list_resources())
print(resources)
print(resources[0])

# create connection
my_instrument = rm.open_resource('ASRL6::INSTR')
# wait for the connection to estavlish
sleep(1)

# request id
print(my_instrument.query('IDN'))