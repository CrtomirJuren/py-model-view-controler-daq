from tkinter.messagebox import NO
from xmlrpc.server import SimpleXMLRPCDispatcher
from pint import test
import serial
from time import sleep

class Device:
    """ """
    DEFAULTS = {
        'baudrate': 9600,
        'read_timeout': 1,
        'write_timeout': 1,
        'write_termination':'\n',
        'read_termination':'\n',
        'encoding':'ascii',
    }

    def __init__(self, port):
        # self.rsc = serial.Serial(port)
        self.port = port

        self.rsc = None
        self.serial_number = None
        
    def initialize(self):
        """[summary]
        """
        self.rsc = serial.Serial()
        self.rsc.port = self.port
        self.rsc.baudrate = self.DEFAULTS.get('baudrate')
        self.rsc.timeout = self.DEFAULTS.get('read_timeout')
        self.rsc.write_timeout = self.DEFAULTS.get('write_timeout')
        self.rsc.open()

        sleep(1)

    def query(self, msg_tx):
        """ sends msg and reads response """
        # create tx message
        msg_tx = msg_tx + self.DEFAULTS.get('write_termination') 
        msg_tx = msg_tx.encode(self.DEFAULTS.get('encoding')) 

        # send tx
        self.rsc.write(msg_tx)
        
        # receive response from device
        msg_rx = self.rsc.readline()
        # bytes to str
        msg_rx = msg_rx.decode(self.DEFAULTS.get('encoding'))
        # remove '\n
        msg_rx = msg_rx.strip()

        return msg_rx

    # public
    def idn(self):
        """ send IDN to device and receive result 
        - method with catching -> happens only once
        """

        # this method is used only once
        if self.serial_number is None:
            self.serial_number = self.query('IDN')

        return self.serial_number

    def get_analog_input(self, channel:int) -> int:
        """ 12bit = 4095 range

        Args:
            channel (int): [description]

        Returns:
            int: 0-1023
        """
        # create message in string format
        msg_tx = f'IN:CH{channel}\n'

        result = self.query(msg_tx)

        # encode msg to bytes before sending
        # msg_tx = msg_tx.encode('ascii')
        # send msg in bytes
        # self.rsc.write(msg_tx)

        # read result from device
        # result = self.rsc.readline().decode('ascii')
        result = int(result)

        return result

    def set_analog_output(self, channel:int, output_value:int) -> None:
        """ range10bit = 1023

        Args:
            channel (int): [description]
            output_value (int): [description]
        """

        msg_tx = f'OUT:CH{channel}:{output_value}\n'
        self.query(msg_tx)

    def finalize(self) -> None:
        """ """
        # if com started
        if self.rsc is not None:
            # close com
            self.rsc.close()

def test_methods():
    # create, open com
    dev = Device('COM6')

    dev.initialize()

    # get idn
    serial_number = dev.idn()
    # here nothing will be sent, because we have idn already stored in class
    serial_number = dev.idn()
    print(f'The device serial number is: {serial_number}')

    # set voltage
    dev.set_analog_output(0, 2000)

    # read 
    ai_value = dev.get_analog_input(0)
    print(f'analog input: {ai_value}')

    dev.finalize()

def test_blink_led():
    # create
    dev = Device('COM6')

    # open com
    dev.initialize()

    # blink 10 times
    for i in range(10):
        # set voltage
        dev.set_analog_output(0, 4000)
        sleep(0.1)
        dev.set_analog_output(0, 0)
        sleep(0.1)

    dev.finalize()

if __name__ == '__main__':
    # test_methods()
    test_blink_led()