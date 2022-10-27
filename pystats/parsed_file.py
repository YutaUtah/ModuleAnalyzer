"""
parsed_file.py

Represents a Python module (aka file).

Parses and stores:
- Lines of code in the module
- Top-level function codeblocks
- Top-level class codeblocks and their respective method codeblocks

"""
try:
#DEBUGGING
    from collections            import namedtuple
    from context.file_context   import FileContext
except:
#COMMANDLINE
    from collections                    import namedtuple
    from pystats.context.file_context   import FileContext


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
        return (
            f'ParsedFile(filename={self.filename}, '
            f'name={self.name}, '
            f'num_lines={len(self.lines)}, '
            f'num_functions={len(self.functions)}, '
            f'num_classes={len(self.functions)}), '
            f'num_methods={len(self.methods)}),'
        )

    def parse(self):
        '''
        Parses the Python module.

        Returns:
            (functions, classes, methods):
                functions: A list of top-level function `ClassBlock`s.
                classes: A list of top-level class `ClassBlock`s.
                methods: A dict mapping each class to a list of method `ClassBlock`s.
        '''
        # Parse the top-level functions and classes
        functions = FileContext.get_functions(self.lines)
        classes = FileContext.get_classes(self.lines)

        # Construct a dictionary mapping each class to its methods
        methods = {}
        for class_block in classes:
            methods[class_block] = FileContext.get_functions(
                class_block.
                lines,  # Assumes `lines` is part of ClassBlock(..., lines=<>)
                indent_level=1,
                offset=class_block.start
            )

        return functions, classes, methods
