import pytest

from pystats import ParsedFile


class TestNumIndents:
    def test_empty(self):
        assert ParsedFile.num_indents('') == 0
        assert ParsedFile.num_indents('    ') == 1

    def test_normal_usage(self):
        assert ParsedFile.num_indents('x = 5') == 0
        assert ParsedFile.num_indents('    x = 5') == 1
        assert ParsedFile.num_indents('    # comment') == 1
        assert ParsedFile.num_indents('        x = 5') == 2

    def test_non_default_indent(self):
        assert ParsedFile.num_indents('\tx = 5', indent='\t') == 1
        assert ParsedFile.num_indents('\t\t\tx = 5', indent='\t') == 3

    def test_ignore_partial_indent(self):
        assert ParsedFile.num_indents(' ') == 0
        assert ParsedFile.num_indents('     ') == 1
        assert ParsedFile.num_indents('          x = 5') == 2
        assert ParsedFile.num_indents('\t\t\t  x = 5', indent='\t') == 3

    def test_empty_indent(self):
        assert ParsedFile.num_indents('x=5', indent='') == 0
