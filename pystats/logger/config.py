from enum import Enum


class Color(Enum):
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"


class Format(Enum):
    LOG_FORMAT = "%(levelname)s:\t %(asctime)s %(message)s (%(filename)s:%(lineno)d %(funcName)s)"


class DisplayFormat(Enum):
    FORMAT = Color.RED.value + Format.LOG_FORMAT.value + Color.RESET.value
