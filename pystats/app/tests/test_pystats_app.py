import unittest

from pystats.app.pystats_app import PyStatsApp


class TestPyStatsApp(unittest.TestCase):
    def setUp(self):
        self.app = PyStatsApp(verbose=False)

    def test_getPaths(self):
        paths = self.app.getPaths(
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils'
        )
        expected_paths = [
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/__init__.py',
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/args_parser.py',
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/format_tree.py',
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/tests/__init__.py',
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/tests/test_args_parser.py',
            '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils/tests/test_format_tree.py',
        ]
        for returned_path, expected_path in zip(paths, expected_paths):
            self.assertEqual(str(returned_path), expected_path)

        self.assertEqual(len(paths), len(expected_paths))

    def test_getPaths_list(self):
        with self.assertRaises(TypeError):
            self.app.getPaths(['this/is/a/wrong/format'])
