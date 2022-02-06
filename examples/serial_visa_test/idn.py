import serial
from serial.tools import list_ports
import time

import snippets

ports = snippets.get_com_list()
print(ports)

# device = serial.Serial('COM6', baudrate=9600)
device = serial.Serial()
device.port = 'COM6'
device.baudrate = 9600
device.timeout = 1
device.open()

time.sleep(1)

device.write(b'IDN\n')
answer = device.readline().decode()
print(f'IDN return: {answer}')

device.close()