import unittest
# from unittest.mock import Mock, MagicMock

from pystats.logger.logger import Logger
from tests.logger.logging_sample import logging_check


class TestLogger(unittest.TestCase):

    def test_basic_config(self):
        logger_default = Logger(__name__).logger
        self.assertEqual(logger_default.name, __name__)
        self.assertEqual(logger_default.level, 20)

        logger_debug = Logger(__name__, level="DEBUG").logger
        self.assertEqual(logger_debug.level, 10)

    def test_log(self):
        with self.assertLogs() as captured:
            logging_check()
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "hello")
        self.assertEqual(captured.records[0].module, "logging_sample")
        self.assertEqual(captured.records[0].funcName, "logging_check")

    def test_level(self):
        logger_default = Logger(__name__).logger
        self.assertEqual(logger_default.getEffectiveLevel(), 20)
        logger_debug = Logger(__name__, level="DEBUG").logger
        self.assertEqual(logger_debug.getEffectiveLevel(), 10)
