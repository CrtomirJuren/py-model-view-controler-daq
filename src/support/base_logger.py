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

if __name__ == '__main__':
    # initalize logger for this module
    logger = logging.getLogger(__name__)
    logger.debug("this is a debug message")
    logger.info("this is an info message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")