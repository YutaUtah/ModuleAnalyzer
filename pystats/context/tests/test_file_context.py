import unittest

from pystats.context.file_context import CodeBlock, FileContext


class TestFileContext(unittest.TestCase):
    """ It is best to precisely define what is meant by the code()
        and len() in the original class.

        Here, we will define them as follows (and revise the class to reflect this):

        - code(): The indented code block, including the signature.
        - len(): The total number of lines in the block, including the signature.

        Therefore, a code block of length 0 has no signature or lines.
    """
    def test_num_indents_empty(self):
        assert FileContext.num_indents('') == 0
        assert FileContext.num_indents('    ') == 1

    def test_num_indents_normal(self):
        assert FileContext.num_indents('x = 5') == 0
        assert FileContext.num_indents('    x = 5') == 1
        assert FileContext.num_indents('    # comment') == 1
        assert FileContext.num_indents('        x = 5') == 2

    def test_num_indents_non_default_indent(self):
        assert FileContext.num_indents('\tx = 5', indent='\t') == 1
        assert FileContext.num_indents('\t\t\tx = 5', indent='\t') == 3

    def test_num_indents_ignore_partial_indent(self):
        assert FileContext.num_indents(' ') == 0
        assert FileContext.num_indents('     ') == 1
        assert FileContext.num_indents('          x = 5') == 2
        assert FileContext.num_indents('\t\t\t  x = 5', indent='\t') == 3

    def test_num_indents_empty_indent(self):
        assert FileContext.num_indents('x=5', indent='') == 0

    def test_codeblock_empty_block(self):
        empty_block = CodeBlock('', '', 0, 0)

        assert len(empty_block) == 0
        assert empty_block.lines == []

    def test_codeblock_public_interface(self):
        cb = CodeBlock('def', 'func()', 37, 38, lines=['def func():'])

        assert len(cb) == 1
        assert cb.lines == ['def func():']

        # Test public interface exists
        assert cb.keyword == 'def'
        assert cb.signature == 'func()'
        assert cb.start == 37
        assert cb.end == 38

    def test_codeblock_optional_lines(self):
        # Line index 10 is `def func():`, up to but not including 15
        cb = CodeBlock('def', 'func()', 10, 15)

        assert len(cb) == 5
        assert cb.lines == []
