import logging
import sys

# COMMANDLINE
# from pystats.utils.logging.config import LEVEL, FORMAT

# DEBUG
from .config import DisplayFormat

'''Outside of this module, you can use: logger = Logger(__file__) '''
class Logger(logging.Formatter):

    LEVEL = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    def __init__(self, filename, level="INFO"):
        self.logger = logging.getLogger(filename)
        self.logger_level = Logger.LEVEL.get(level.upper())
        self._get_custom_logger()

    def _setLevel(self, logger_level):
        self.logger.setLevel(logger_level)

    def _add_stream_Handler(self):
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter(DisplayFormat.FORMAT.value))
        self.logger.addHandler(ch)

    def _get_custom_logger(self):
        self._setLevel(self.logger_level)
        if not self.logger.handlers:
            self._add_stream_Handler()


    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def is_valid_logger(self, level, log):
        if isinstance(self.getEffectiveLevel(), int):
            return self.getEffectiveLevel() <= Logger.LEVEL.get(level) and len(log) > 0
        return False

    def debug(self, log):
        if self.is_valid_logger("DEBUG", log):
            self.logger.debug(log)
        else:
            self.logger.error("Text log is empty")

    def info(self, log):
        if self.is_valid_logger("INFO", log):
            self.logger.info(log)
        else:
            self.logger.error("Text log is empty")

    def warning(self, log):
        if self.is_valid_logger("WARNING", log):
            self.logger.warning(log)
        else:
            self.logger.error("Text log is empty")

    def error(self, log):
        if self.is_valid_logger("ERROR", log):
            self.logger.error(log)
        else:
            self.logger.error("Text log is empty")

    def critical(self, log):
        if self.is_valid_logger("CRITICAL", log):
            self.logger.critical(log)
        else:
            self.logger.error("Text log is empty")

