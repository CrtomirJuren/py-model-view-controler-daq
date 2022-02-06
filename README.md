# libraries
PINT
- physical units
- https://pint.readthedocs.io/en/stable/tutorial.html

SERIAL
- https://pyserial.readthedocs.io/en/latest/

VISA
- https://pyvisa.readthedocs.io/en/1.8/tutorial.html

LANTZ
- https://lantz.readthedocs.io/en/0.3/


# STEPS TO WRITING A DRIVER : python-arduino serial driver

- first write basic command in arduino
- test the command over arduino serial port
- write python script to test single command
- add a method to python class
- start the steps again for every single command. dont do all commands at once 


# list all devices on COM ports from terminal
```
python -m serial.tools.list_ports
```

# run miniterm for debbuging device from cmd
```
(pftl) C:\Users\crtom\Documents\python\py-model-view-controler-daq>python -m serial.tools.miniterm -h
```