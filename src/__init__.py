print('executed src\__init__.py')
import time
import numpy as np
from pathlib import Path

# --- parent logging module ---
import logging

DEBUG = True

# create parent logger
logger = logging

# configure logger
if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format='%(name)10s.%(funcName)-8s | %(levelname)-7s | %(message)s')
else:
    # for finished app
    logging.basicConfig(level=logging.INFO, format ='%(message)s')

# used for daq physical units
import pint
ur = pint.UnitRegistry()
V = ur('V')
mV = ur('mV')


