from src import *

import sys, os
from pathlib import Path
import pyqtgraph as pg

from src.model.experiment import Experiment

# create experiment
experiment = Experiment('src\experiment.yml')

# load config file
experiment.load_config()
logger.debug(experiment.config)

# load daq
experiment.load_daq()
logger.info(experiment.daq)

# create plot
PlotWidget = pg.plot(title = 'title')
PlotWidget.setLabel('bottom','a')
PlotWidget.setLabel('left','b')
PlotWidget.setRange(xRange=[0,20])
# scan
# this is obsolete because of threading
# experiment.do_scan() 
experiment.start_scan()

while experiment.scan_is_running:
    logger.debug('Experiment running')
    # update graph data
    PlotWidget.plot(experiment.scan_range.m_as('V'), experiment.scan_data.m_as('V'), clear = True)
    # pg.QtGui.QAppplication.processEvents()
    pg.QtGui.QApplication.processEvents()
    time.sleep(1)

# end experiment
experiment.finalize()

# save data at end of experiment
experiment.save_data()

# for this to stay opened you must run script interactive
# -i -> interactive mode
""" python -i /path/to/script.py """
""" python -i src\model\experiment.py """
