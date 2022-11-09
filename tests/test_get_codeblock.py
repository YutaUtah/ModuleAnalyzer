from collections import namedtuple
import unittest
from parameterized import parameterized


from pystats.context.file_context import CodeBlock, FileContext


class TestGetCodeBlocks(unittest.TestCase):
    CodeTestCase = namedtuple(
        'CodeTestCase',
        ['keyword', 'indent_level', 'offset', 'expected', 'code']
    )

    NO_CODE = CodeTestCase(
        keyword='class',
        indent_level=0,
        offset=0,
        expected=[],
        code=[]
        )

    NO_BLOCKS = CodeTestCase(
        keyword='class',
        indent_level=0,
        offset=0,
        expected=[],
        code=[
            '',
            'x = 5',
            'y = 10',
            '',
        ])

    ONE_DEF_BLOCK = CodeTestCase(
        keyword='class',
        indent_level=0,
        offset=0,
        expected=[CodeBlock('class', 'Identity', 0, 3)],
        code=[
            'class Identity:',
            '    def id(x):',
            '        return x',
            'print("end")',
        ])

    TWO_DEF_BLOCKS = CodeTestCase(
        keyword='def',
        indent_level=0,
        offset=0,
        expected=[
            CodeBlock('def', 'identity(x)', 0, 2),
            CodeBlock('def', 'mul(x, y)', 2, 4),
        ],
        code=[
            'def identity(x):',
            '    return x',
            'def mul(x, y):',
            '    return x * y',
        ])

    EMPTY_LINE_OFFSET_BLOCKS = CodeTestCase(
        keyword='def',
        indent_level=0,
        offset=1,
        expected=[
            CodeBlock('def', 'identity(x)', 3, 6),  # +1 offset
            CodeBlock('def', 'mul(x, y)', 8, 11),  # +1 offset
        ],
        code=[
            '',
            'print("start")',
            'def identity(x):',
            '    return x',
            '',
            'print("middle")',
            '',
            'def mul(x, y):',
            '    return x * y',
            '',
        ])

    INDENTED_BLOCK = CodeTestCase(
        keyword='def',
        indent_level=1,
        offset=0,
        expected=[
            CodeBlock('def', 'internal()', 3, 5),
            CodeBlock('def', 'test_this(name)', 7, 10),
        ],
        code=[
            '',
            'print("start")',
            'def closure(x):',
            '    def internal():',
            '        return x',
            '    return internal',
            'class Test:',
            '    def test_this(name):',
            '        return name',
            '',
        ])

    ALL_EXAMPLES = [
        NO_CODE,
        NO_BLOCKS,
        ONE_DEF_BLOCK,
        TWO_DEF_BLOCKS,
        EMPTY_LINE_OFFSET_BLOCKS,
        INDENTED_BLOCK
    ]

    @parameterized.expand(ALL_EXAMPLES)
    def test_something(self, keyword, indent_level, offset, expected, code):
        blocks = FileContext.get_codeblocks(code, keyword, indent_level, offset)
        self.assertEqual(blocks, expected)
