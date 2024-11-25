from datetime import datetime
import logging
import traceback


def get_now_date_time():
    """
    Returns formatted current data and time.
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    return dt_string


def configure_logger():
    """
    Run basic configuration of logger.
    """
    logging.basicConfig(filename=f'logs/pipeline_{get_now_date_time()}.log',
                        encoding='utf-8', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def get_logger(name, level='debug'):
    """
    Gets logger with specified name and logging level.
    """
    valid_levels = ('debug', 'info', 'warning', 'error', 'critical')

    logger = logging.getLogger(name)
    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif level == 'info':
        logger.setLevel(logging.INFO)
    elif level == 'warning':
        logger.setLevel(logging.WARNING)
    elif level == 'error':
        logger.setLevel(logging.ERROR)
    elif level == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        raise ValueError(
            f'Invalid logging level received. Valid levels are: {valid_levels}')

    return logger


def log_error(logger, error):
    """
    Logs error to log file and prints error traceback
    """
    logger.error(f'An error occurred: {error}')
    traceback.print_exc()
