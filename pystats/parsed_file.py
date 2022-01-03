"""
parsed_file.py

Represents a Python module (aka file). 

Parses and stores:
- Lines of code in the module
- Top-level function codeblocks
- Top-level class codeblocks and their respective method codeblocks

"""

from collections import namedtuple


# This class should be a drop-in replacement for `namedtuple`,
#   with the exception of the optional `lines` attribute.
class CodeBlock:
    """A block of Python code.

    Attributes:
        keyword: The type of code block (e.g. 'def', 'class').
        signature: The text between the keyword and colon, i.e. <keyword><signature>:
        start: The first line index into the module.
        end: The final line index into the module (exclusive).
        lines: Optionally, a list of lines of text comprising the code block and signature.

    """

    # Note the new optional paramter 'lines'.
    def __init__(self, keyword, signature, start, end, lines=[]):
        self.keyword = keyword
        self.signature = signature
        self.start = start
        self.end = end
        self.lines = lines

    # Called when run: `len(code_block)`
    # Return the total number of lines, including the signature.
    def __len__(self):
        # Compute since `lines` is optional.
        # Should be the same as `len(self.lines)`
        return self.end - self.start

    def __repr__(self):
        return (f'CodeBlock(signature={self.signature}, '
                f'num_lines={len(self)},'
                f'start={self.start}, '
                f'end={self.end}')

    def __eq__(self, other):
        """
        Returns True if `self` and `other` are the same `CodeBlock`.
        - `lines` is ignored since it is optional.
        """
        return self.keyword == other.keyword and \
               self.signature == other.signature and \
               self.start == other.start and \
               self.end == other.end

    def __hash__(self):
        """
        Returns a number representing the object's value.
        - This allows `CodeBlock` to be used as a dict key.
        """
        return hash((self.keyword, self.signature, self.start, self.end))


class ParsedFile:
    """Represents a Python module (aka file).

    Parses and stores:
    - Lines of code in the module
    - Top-level function codeblocks
    - Top-level class codeblocks and their respective method codeblocks

    Public Attributes:
        functions: A list of top-level function `ClassBlock`s.
        classes: A list of top-level class `ClassBlock`s.
        methods: A dict mapping each class to a list of method `ClassBlock`s.
    """

    ########################
    # Class Variables
    # - Refer to these as: ParsedFile.INDENT
    ########################
    INDENT = '    '

    ########################
    # Static Methods
    # - Refer to these as: ParsedFile.num_indents(line)
    ########################
    @staticmethod
    def num_indents(line, indent=INDENT):
        """ 
        Counts how many times `indent` repeats at the start of `line`.

        Ignores partial indents, even though they may be invalid Python.

        Args:
            line: A line of Python code.
            indent: A string denoting one indentation level.

        Returns:
            The indentation level of the line of code.
        """
        nchars = len(indent)
        if nchars == 0:
            return 0

        i = 0
        while i <= len(line) and line[i:i + nchars] == indent:
            i += nchars

        return i // nchars


    # Note there is a new `offset` parameter.
    # This adds `offset` to the start and end indexes.
    # This is intended to allow for absolute indexes, instead of them being relative to a parent.
    @staticmethod
    def get_codeblocks(lines, keyword, indent_level=0, offset=0):
        """Parses `lines` to retrieve `CodeBlock`s starting with `keyword`.

        Args:
            lines: Lines of Python code.
            keyword: The Python keyword beginning a code block.
            indent_level: Retrieves only blocks beginning at this indentation level.
            offset: Adds a fixed offset to the start and end indexes.

        Returns:
            A list of `CodeBlock`s.
        """
        block_prefix = ParsedFile.INDENT * indent_level + keyword
        block_sig = ''
        block_start = 0

        blocks = []
        for i, line in enumerate(lines):
            # Skip lines that are entirely whitespace
            if line.strip():
                # Inside a block
                if block_sig:
                    if ParsedFile.num_indents(line) <= indent_level:
                        block_lines = lines[block_start:i]
                        blocks.append(
                            CodeBlock(keyword,
                                      block_sig,
                                      block_start + offset,
                                      i + offset,
                                      lines=block_lines))
                        block_sig = ''

                # Start of a new block
                if line.startswith(block_prefix):
                    # The signature excludes the prefix and ':'
                    block_sig = line[len(block_prefix):].strip()[:-1]
                    block_start = i

        # If still inside a block, add the block
        if block_sig:
            block_lines = lines[block_start:i + 1]
            blocks.append(
                CodeBlock(keyword,
                          block_sig,
                          block_start + offset,
                          i + offset + 1,
                          lines=block_lines))

        return blocks

    @staticmethod
    def get_functions(lines, indent_level=0, offset=0):
        """Returns a list of `CodeBlock` functions at `indent_level`, relative to line index `offset`."""
        return ParsedFile.get_codeblocks(lines,
                                         'def',
                                         indent_level=indent_level,
                                         offset=offset)

    @staticmethod
    def get_classes(lines, indent_level=0, offset=0):
        """Returns a list of `CodeBlock` classes at `indent_level`, relative to line index `offset`."""
        return ParsedFile.get_codeblocks(lines,
                                         'class',
                                         indent_level=indent_level,
                                         offset=offset)

    ########################
    # Public Methods
    ########################

    def __init__(self, filename, lines):
        """Initializes and parses the list of `lines`.

        Assumes they are a Python module named `name` (typically the name of the file).
        """
        self.filename = filename
        self.lines = lines

        # Assume the module name is the filename without an extension
        self.name = filename.strip().rsplit('.', maxsplit=1)[0]

        self.functions, self.classes, self.methods = self.parse()

    def __repr__(self):
        return (f'ParsedFile(filename={self.filename}, '
                f'name={self.name}, '
                f'num_lines={len(self.lines)}, '
                f'num_functions={len(self.functions)}, '
                f'num_classes={len(self.functions)})')

    def parse(self):
        """Parses the Python module.

        Returns: 
            (functions, classes, methods):
                functions: A list of top-level function `ClassBlock`s.
                classes: A list of top-level class `ClassBlock`s.
                methods: A dict mapping each class to a list of method `ClassBlock`s.
        """
        # Parse the top-level functions and classes
        functions = ParsedFile.get_functions(self.lines)
        classes = ParsedFile.get_classes(self.lines)

        # Construct a dictionary mapping each class to its methods
        methods = {}
        for class_block in classes:
            methods[class_block] = ParsedFile.get_functions(
                class_block.
                lines,  # Assumes `lines` is part of ClassBlock(..., lines=<>)
                indent_level=1,
                offset=class_block.start)

        return functions, classes, methods
