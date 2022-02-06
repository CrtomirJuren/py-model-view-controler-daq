from xmlrpc.server import SimpleXMLRPCDispatcher
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
        self.rsc = serial.Serial()
        self.rsc.port = self.port
        self.rsc.baudrate = self.DEFAULTS.get('baudrate')
        self.rsc.timeout = self.DEFAULTS.get('read_timeout')
        self.rsc.write_timeout = self.DEFAULTS.get('write_timeout')
        self.rsc.open()

        sleep(1)

    # private
    def query(self, msg_tx):
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

        if self.serial_number is None:
            # # send IDN request to device
            # self.rsc.write(b'IDN\n')
            # # get answer from device 
            # msg_rx = self.rsc.readline()
            # # decode from bytes to str
            # msg_rx = msg_rx.decode('ascii')
            # # remove '\n'
            # msg_rx = msg_rx.strip()

            # self.serial_number = msg_rx
            self.serial_number = self.query('IDN')
        else:
            # do nothing
            pass

        # print(self.idn)
        return self.serial_number

    def get_analog_input(self, channel:int) -> int:
        """[summary]

        Args:
            channel (int): [description]

        Returns:
            int: 0-1023
        """
        # create message in string format
        msg_tx = f'IN:CH{channel}\n'
        # encode msg to bytes before sending
        msg_tx = msg_tx.encode('ascii')
        # send msg in bytes
        self.rsc.write(msg_tx)

        # read result from device
        result = self.rsc.readline().decode('ascii')
        result = int(result)

        return result

    def set_analog_output(self, channel:int, output_value:int):
        msg_tx = f'OUT:CH{channel}:{output_value}\n'
        msg_tx = msg_tx.encode('ascii')

        self.rsc.write(msg_tx)

        # because arduino code returns value after voltage is set
        # we need to read this from serial buffer
        self.rsc.readline()

if __name__ == '__main__':
    # create, open com
    dev = Device('COM6')

    dev.initialize()

    # get idn
    serial_number = dev.idn()
    # here nothing will be sent, because we have idn already stored in class
    serial_number = dev.idn()
    print(f'The device serial number is: {serial_number}')

    # set voltage
    dev.set_analog_output(0, 512)

    # read 
    ai_value = dev.get_analog_input(0)
    print(f'analog input: {ai_value}')
