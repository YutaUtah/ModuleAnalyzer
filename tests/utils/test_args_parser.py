import unittest

from pystats.utils.args_parser import add_parser_options
from pystats.context.package_context import PackageContext


class TestGetCodeBlocks(unittest.TestCase):

    def test_add_parser_options(self):
        app = add_parser_options(PackageContext)
        args = app.parse_args('-h')
        self.assertEqual(args.input, ['-', 'h'])
