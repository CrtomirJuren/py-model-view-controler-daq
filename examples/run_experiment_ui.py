from src import *

import sys, os
from pathlib import Path
import pyqtgraph as pg

from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, 
                            QPushButton,
                            QMainWindow,
                            QWidget,
                            QHBoxLayout,
                            QVBoxLayout,
                            )

from src.model.experiment import Experiment

logger = logging.getLogger(__name__)

# Screen resolution
res_W = 1920
res_H = 1080
win_W = 800
win_H = 500

# constants for center of screen
res_WH = res_W // 2
res_HH = res_H // 2
win_pos_W = res_WH - (win_W // 2)
win_pos_H = res_HH - (win_H // 2)

class MainWindow(QMainWindow):
    """ 
    When creating instance of class, we pass it a window reference.
    This becomes win -> self. Can be confusing.
    Transforms:
    win.setWindowTitle("") --> self.setWindowTitle("")
    QtWidgets.QLabel(win) --> QtWidgets.QLabel(self)
    """
    def __init__(self, experiment = None):
        super(MainWindow, self).__init__()
        
        self.experiment = experiment

        self.setGeometry(win_pos_W, win_pos_H, win_W, win_H)
        self.setWindowTitle("U-I Led DAQ Experiment")
        self.initUI()
        
        # create timer for plot update
        self.timer_plot_update = QTimer()
        self.timer_plot_update.timeout.connect(self.update_plot)
        self.timer_plot_update.start(50) #ms

    def initUI(self):
        # --------------------------------------
        # --- create buttons widget - layout ---
        # create buttons layout
        self.button_widgets = QWidget()
        button_layout = QHBoxLayout(self.button_widgets)

        # --- button 1 ---
        b1 = QPushButton("Start Scan",self.button_widgets)
        # connect signal to slot
        b1.clicked.connect(self.start_scan_event)

        b2 = QPushButton("Stop Scan")
        b2 = QPushButton("Stop Scan")
        # connect signal to slot
        b2.clicked.connect(self.stop_scan_event)

        b3 = QPushButton("Save Data")
        # connect signal to slot
        b3.clicked.connect(self.save_data_event)

        b4 = QPushButton("Exit App")
        # connect signal to slot
        b4.clicked.connect(self.exit_app_event)
        # changing color of button
        b4.setStyleSheet("background-color : pink")

        # add buttons to button layout
        button_layout.addWidget(b1)
        button_layout.addWidget(b2)
        button_layout.addWidget(b3)
        button_layout.addWidget(b4)
        
        # -----------------------------------
        # --- create plot widget - layout ---
        self.plot_widget = pg.PlotWidget(title = 'Led Diode U-I Plot')
        self.plot = self.plot_widget.plot([0],[0])

        # ---------------------------
        # --- main central layout ---
        self.central_widget = QWidget()

        # create centarl layout
        central_layout = QVBoxLayout(self.central_widget)

        # add other widgets-layouts to central layout
        central_layout.addWidget(self.plot_widget)
        central_layout.addWidget(self.button_widgets)

        # Set the layout on the application's window
        self.setCentralWidget(self.central_widget)

    # slot
    def start_scan_event(self):
        logger.debug('start_scan_event')
        # scan
        self.experiment.start_scan()
    
    # slot
    def exit_app_event(self):
        logger.debug('exit_app_event')

        # close application
        self.close()

    # slot
    def save_data_event(self):
        logger.debug('save_data_event')

        # save data at end of experiment
        self.experiment.save_data()

    # slot
    def stop_scan_event(self):
        logger.debug('stop_scan_event')

        # save data at end of experiment
        self.experiment.stop_scan()

    # slot
    def update_plot(self):
        # x = self.experiment.scan_range
        # y = 

        self.plot.setData(self.experiment.scan_range.m_as(V),
                          self.experiment.scan_data.m_as(V))

def window():
    # --- initialize experiment ---
    # create experiment
    experiment = Experiment('src\experiment.yml')

    # load config file
    experiment.load_config()
    logger.debug(experiment.config)

    # load daq
    experiment.load_daq()
    logger.info(experiment.daq)

    # --- start GUI ---
    app = QApplication(sys.argv) # app setup
    #win = QMainWindow()
    win = MainWindow(experiment)
    win.show()
    sys.exit(app.exec_()) # clean app exit
    
    # end experiment
    experiment.finalize()

# start app
window()









