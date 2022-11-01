import unittest
from unittest.mock import Mock, MagicMock

import pystats.statistic as statistic
from pystats.parsed_file import CodeBlock


class TestStats(unittest.TestCase):
    def test_num_module_lines(self):
        parsed_file = MagicMock(name='ParsedFile')
        parsed_file.lines = []

        calculated_stat = statistic.NumModuleLines(parsed_file)
        # empty lines in the parsed file
        assert '**Num Module Lines:** 0' in calculated_stat.module_stats

        parsed_file.lines = [
            'year = 2021',
            '# 10 years later',
            'print(year+10)',
            '',
            'print(year*10)'
        ]
        calculated_stat = statistic.NumModuleLines(parsed_file)
        # 5 lines in the parsed file
        assert '**Num Module Lines:** 5' in calculated_stat.module_stats

    def test_num_func_lines(self):
        parsed_file = MagicMock(name='ParsedFile')
        parsed_file.functions = [
            CodeBlock(
                keyword='def',
                signature='def test_func(self, a, b):',
                start=1,
                end=5,
                lines=[
                    'def func(a, b):',
                    'c = a + b',
                    'd = a * b',
                    'return c + d',
                ]
            ),

            CodeBlock(keyword='def',
                      signature='def hello(name):',
                      start=5,
                      end=7,
                      lines=['def circle_area(r):',
                             'return r * r * 3.14'])
        ]

        calculated_stat = statistic.NumFuncLines(parsed_file)
        first_function = parsed_file.functions[0]
        second_function = parsed_file.functions[1]

        assert '**Num Function Lines:** 4' in calculated_stat.function_stats[first_function]
        assert '**Num Function Lines:** 2' in calculated_stat.function_stats[second_function]

    def test_num_method_lines(self):
        parsed_file = MagicMock(name='ParsedFile')

        # Test empty Python file
        parsed_file.classes = []
        parsed_file.methods = {}

        calculated_stat = statistic.NumMethodLines(parsed_file)
        assert len(calculated_stat.function_stats) == 0

        # test Python file with 1 class and 1 method
        class_with_one_class = CodeBlock(
                                    keyword='class',
                                    signature='class One',
                                    start=0,
                                    end=3,
                                    lines=[
                                        'class One:',
                                        'def __init__(self, x)',
                                        'self.one = x'
                                    ]
                                )

        method_with_one_method = CodeBlock(
                                        keyword='def',
                                        signature='def __init__(self, x)',
                                        start=1,
                                        end=3,
                                        lines=[
                                            'def __init__(self, x)',
                                            'self.one = x'
                                        ]
                                )

        parsed_file.classes = [class_with_one_class]
        parsed_file.methods = {class_with_one_class: [method_with_one_method]}
        calculated_stat = statistic.NumMethodLines(parsed_file)
        assert "**Num Method Lines:** 2" in calculated_stat.function_stats[method_with_one_method]

    def test_num_class_lines(self):
        parsed_file = Mock(name='ParsedFile')

        # Test empty Python file
        parsed_file.classes = []
        parsed_file.methods = {}

        calculated_stat = statistic.NumClassLines(parsed_file)
        assert len(calculated_stat.class_stats) == 0

        # test Python file with 1 class and 1 method
        class_with_one_class = CodeBlock(keyword='class',
                                         signature='class One',
                                         start=0,
                                         end=3,
                                         lines=['class One:',
                                                'def __init__(self, x)',
                                                'self.one = x'
                                                ]
                                         )
        method_with_one_method = CodeBlock(keyword='def',
                                           signature='def __init__(self, x)',
                                           start=1,
                                           end=3,
                                           lines=['def __init__(self, x)',
                                                  'self.one = x']
                                           )

        parsed_file.classes = [class_with_one_class]
        parsed_file.methods = {class_with_one_class: [method_with_one_method]}
        calculated_stat = statistic.NumClassLines(parsed_file)
        assert "**Num Class Lines:** 3" in calculated_stat.class_stats[class_with_one_class]
        assert "**Num Methods:** 1" in calculated_stat.class_stats[class_with_one_class]

    def test_dunder_method(self):
        parsed_file = Mock(name='ParsedFile')

        calculated_stat = statistic.dunderMethodPythonPackage(parsed_file)
        assert '**dunder method in the package:** 1' in calculated_stat.package_stats[0]
