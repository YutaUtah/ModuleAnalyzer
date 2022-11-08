import unittest
# from unittest.mock import Mock, MagicMock

from pystats.logger.logger import Logger


class TestLogger(unittest.TestCase):

    def test_basic_config(self):
        logger_default = Logger(__name__).logger
        self.assertEqual(logger_default.name, __name__)
        self.assertEqual(logger_default.level, 20)

        logger_debug = Logger(__name__, level="DEBUG").logger
        self.assertEqual(logger_debug.level, 10)
        # print(logger.name)
