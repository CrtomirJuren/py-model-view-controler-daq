import serial
import serial.tools.list_ports

#No serial port returns 0,
#Returns the list of available serial ports
def get_com_list():

    port_list = list(serial.tools.list_ports.comports())

    for port, desc, hwid in sorted(port_list):
            print("found {}: {} [{}]".format(port, desc, hwid))
            
    # The function returns a list of ListPortInfo objects.
    return port_list