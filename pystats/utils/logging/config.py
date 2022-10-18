import logging

class Color:
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

class LoggerProperty:
    FORMAT = "%(levelname)s:\t %(asctime)s %(message)s (%(filename)s:%(lineno)d)"

LEVEL = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

FORMAT = {
    logging.DEBUG: Color.RED + LoggerProperty.FORMAT + Color.RESET,
    logging.INFO: Color.RED + LoggerProperty.FORMAT + Color.RESET,
    logging.WARNING: Color.RED + LoggerProperty.FORMAT + Color.RESET,
    logging.ERROR: Color.RED + LoggerProperty.FORMAT + Color.RESET,
    logging.CRITICAL: Color.BOLD_RED + LoggerProperty.FORMAT + Color.RESET,
}