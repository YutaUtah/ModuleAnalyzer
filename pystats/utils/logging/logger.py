import logging
import sys

# COMMANDLINE
# from pystats.utils.logging.config import LEVEL, FORMAT

# DEBUG
from .config import LEVEL, FORMAT


class CustomFormatter(logging.Formatter):
    datefmt='%I:%M:%S %p %m/%d/%Y'
    FORMATS = FORMAT
    stream=sys.stdout

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class CustomLogger:
    def __init__(self, level):
        self.logger = logging.getLogger(__name__)
        self.custom_format = CustomFormatter()
        self.logger_level = LEVEL.get(level.upper())

    def _setLevel(self, logger_level):
        self.logger.setLevel(logger_level)

    def _addStreamHandler(self):
        ch = logging.StreamHandler()
        ch.setFormatter(self.custom_format)
        self.logger.addHandler(ch)
        self.logger.propagate = False

    def get_custom_logger(self):
        self._setLevel(self.logger_level)
        if not self.logger.handlers:
            self._addStreamHandler()
        return self.logger

