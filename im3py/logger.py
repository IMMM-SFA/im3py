import logging
import sys


class Logger:
    """Initialize project-wide logger. The logger outputs to both stdout and a file.

    :param logfile:                             Full path with file name and extension to the log file.

    """

    def __init__(self, logfile):

        self._logfile = logfile

    def initialize_logger(self):
        """Initialize logger to stdout and file."""

        # set format
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # init logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # logger console handler
        c_handler = logging.StreamHandler(sys.stdout)
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(log_format)
        logger.addHandler(c_handler)

        # logger file handler
        f_handler = logging.FileHandler(self._logfile)
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(log_format)
        logger.addHandler(f_handler)

    @staticmethod
    def close_logger():
        """Shutdown logger."""

        # Remove logging handlers
        logger = logging.getLogger()

        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        logging.shutdown()
