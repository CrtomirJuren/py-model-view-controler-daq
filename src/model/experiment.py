"""

"""
from concurrent.futures import thread
from src import *
import pyqtgraph as pg #conda install -c anaconda pyqtgraph
from datetime import datetime
import yaml #conda install -c anaconda yaml
import csv
import threading

logger = logging.getLogger(__name__)

class Experiment:

    def __init__(self, config_file):
        # driver
        self.daq = None
        self.scan_thread = None
        
        # configuration
        self.config_file = config_file
        self.config = None

        # data
        self.scan_range = np.array([0]) *V
        self.scan_data = np.array([0]) *V

        # flags
        self.scan_is_running = False
        self.scan_stop_interrupt = False

    def load_config(self):
        logger.debug('loading experiment configuration')
        
        with open(self.config_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.config = data

        # here after loading configuration, raiseError if something missing
        # if empty data, raise error
        if not self.config:
            raise IOError('experiment.yaml file is empty')

    def load_daq(self):
        # daq_config = self.config['DAQ']
        name = self.config['DAQ']['name']
        port = self.config['DAQ']['port']

        logger.info(f'Loaded {name} from config')

        # load DAQ
        if name == 'AnalogDaq':
            from src.model.daq_hal.daq_analog import AnalogDaq
            self.daq = AnalogDaq ('COM6')
        elif name == 'SimDaq':
            from src.model.daq_hal.daq_sim import SimDaq
            # from daq_sim import SimDaq
            self.daq = SimDaq('sine')
        else:
            raise Exception(f' {name} module not implemented or found.')
            # here put logging error
            # logging.critical()
        
        # initialize DAQ
        self.daq.initialize()

    def start_scan(self):
        logger.debug('start scan requested')
        self.scan_stop_interrupt = False
        self.scan_is_running = False

        # create thread
        self.scan_thread = threading.Thread(target = self.do_scan)
        # start thread
        self.scan_thread.start()

    def stop_scan(self):
        # set flag interrupt only if scan is running
        if self.scan_is_running:
            self.scan_stop_interrupt = True

    def do_scan(self):
        """ """
        # --- if scan is not running ---
        if self.scan_is_running:
            logger.info('Scan already running. Not started.')
            # exit function/thread
            return
        # --- if scan is running ---
        else:
            logger.info('Scan started.')
            self.scan_is_running = True
            # # get data from experiment.yml file
            # DEVICE IO PINS
            ch_out =  self.config['Scan']['channel_out']
            ch_in =  self.config['Scan']['channel_in']
            
            # #ur = UnitRegistry() from pint
            start = self.config['Scan']['start']
            # # str -> voltage
            start = ur(start).m_as('V')

            stop = self.config['Scan']['stop']
            # # str -> voltage
            stop = ur(stop).m_as('V')
            num_steps = int(self.config['Scan']['num_steps'])

            # # delay between voltage steps
            delay = self.config['Scan']['delay']
            delay = ur(delay).m_as('s')

            # create array in volts
            self.scan_range = np.linspace(start, stop, num_steps)*V
            
            # create buffer to store data in volts
            self.scan_data = np.zeros(num_steps) * V

            # start plot updates
            for index, volt_out in enumerate(self.scan_range):

                logger.debug(f'{index}, {volt_out:.3f}')
                # set voltage to output
                self.daq.set_voltage(ch_out, volt_out)
                # read measurement -> returns volts
                volt_meas = self.daq.get_voltage(ch_in)
                
                # save measurement to buffer
                self.scan_data[index] = volt_meas
                time.sleep(delay)
                
                if self.scan_stop_interrupt:
                    logger.info('Scan interrupted')
                    break

            # only if for loop was not interrupted
            else:
                # when scan is finished reset running flag
                logger.info('Scan finished')
            
            self.scan_is_running = False
            # when scan is finished, set voltage back to 0
            self.daq.set_voltage(ch_out, 0*V)
           
    def save_data(self):
        # main log folder
        data_folder = Path(self.config['Saving']['folder'])
        filename = Path(self.config['Saving']['filename'])
        append_timestamp = self.config['Saving']['timestamp']
        append_suffix = self.config['Saving']['suffix']

        # create monthly folder to organize logs
        now = datetime.today()
        month = now.strftime('%Y-%m')
        saving_folder = data_folder/month
        
        # create monthly folder
        # parents=True create any parent folders that are missing
        # exist_ok=True if folder already exist, ignore errors
        saving_folder.mkdir(parents=True, exist_ok=True)

        filepath = saving_folder / filename

        base_name = filepath.stem
        extension = filepath.suffix

        i = 1
        while filepath.is_file():
            filepath = saving_folder / f"{base_name}_{i}{extension}"
            # filename = f'{base_name}_{i:03d}.{extension}'
            i += 1

        data = np.vstack([self.scan_range, self.scan_data]).T 
        # remove volts from data
        data = data.m_as(V)

        logger.debug(f'saving data to: {filepath}')
        
        np.savetxt(filepath, 
            data, 
            delimiter = ',',
            fmt = '%.5f', 
            header = 'a,b',
            comments='')

    def finalize(self):
        logger.debug('Finalizing Experiment')
        # stop do_scan thread
        self.stop_scan()
        while self.scan_is_running:
            time.sleep(0.1)
            
        self.daq.finalize()

# if __name__ == '__main__':
#     # create experiment
#     experiment = Experiment('src\experiment.yml')
    
#     # load config file
#     experiment.load_config()
#     logger.debug(experiment.config)
    
#     # load daq
#     experiment.load_daq()
#     logger.info(experiment.daq)

#     # scan
#     experiment.do_scan()

#     # end experiment
#     experiment.finalize()

#     # save data at end of experiment
#     experiment.save_data()

#     # for this to stay opened you must run script interactive
#     # -i -> interactive mode
#     """ python -i /path/to/script.py """
#     """ python -i src\model\experiment.py """
#     pg.plot(experiment.scan_range, experiment.scan_data)