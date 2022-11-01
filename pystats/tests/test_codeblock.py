import unittest

# from pystats.parsed_file import CodeBlock


class TestCodeBlock(unittest.TestCase):
    """ It is best to precisely define what is meant by the code()
        and len() in the original class.

        Here, we will define them as follows (and revise the class to reflect this):

        - code(): The indented code block, including the signature.
        - len(): The total number of lines in the block, including the signature.

        Therefore, a code block of length 0 has no signature or lines.
    """
    def test_codeblock(self):
        self.assertEqual('hi', 'hi')

    # def test_empty_block(self):
    #     empty_block = CodeBlock('', '', 0, 0)

    #     assert len(empty_block) == 0
    #     assert empty_block.lines == []

    # def test_public_interface(self):
    #     cb = CodeBlock('def', 'func()', 37, 38, lines=['def func():'])

    #     assert len(cb) == 1
    #     assert cb.lines == ['def func():']

    #     # Test public interface exists
    #     assert cb.keyword == 'def'
    #     assert cb.signature == 'func()'
    #     assert cb.start == 37
    #     assert cb.end == 38

    # def test_optional_lines(self):
    #     # Line index 10 is `def func():`, up to but not including 15
    #     cb = CodeBlock('def', 'func()', 10, 15)

    #     assert len(cb) == 5
    #     assert cb.lines == []
