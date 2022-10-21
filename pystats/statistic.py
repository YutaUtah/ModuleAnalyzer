'''
statistic.py

Statistics computed on a `ParsedFile`.

Each class inherits from `Statistic` and individually computes a statistic.

To add a new stat:
1. Create a new class derived from `Statistic`.
2. Implement the `name()` and `compute(self)` methods.
3. Register the stat with the command-line program in `pystats.py`.
'''

from abc         import ABCMeta, abstractmethod
from collections import defaultdict

#COMMANDLINE
# from pystats.utils.logging.logger import Logger
#DEBUGGING
from utils.logging.logger import Logger

logger = Logger(__name__).logger


class Statistic(metaclass=ABCMeta):
    """An abstract base class representing a statistic computed on a `ParsedFile`."""
    def __init__(self, parsed_file):
        """Initializes a `Statistic` and computes the stat immediately."""
        self.parsed_file = parsed_file

        # To add stats, append Markdown text to the appropriate stats section.

        # `module_stats`: A list of strings placed next to the module name
        # - Example: ['**Num Lines:** 8', '**Num Vars**: 100']
        self.module_stats = []
        # `function_stats`: A dict mapping a function `CodeBlock` to a list of stat strings
        # - Example: {func_block: ['**Num Lines:** 12, ...]}
        self.function_stats = defaultdict(list)
        # `class_stats`: A dict mapping a class `CodeBlock` to a list of stat strings
        # - Example: {class_block: ['**Num Lines:** 38, ...]}
        self.class_stats = defaultdict(list)
        # `package_stats`: A list of string that displays the number of dunder methods
        # - Example: ['**dunder method in the package:** {dunderMethod}']
        self.package_stats = []

        # Compute the stat immediately
        self.compute()

    def __repr__(self):
        return (
            f'Statistic(name={self.name()}, \n'
            f'          module={self.parsed_file.name}, \n'
            f'          module_stats={self.module_stats}, \n'
            f'          function_stats={ {f.signature: stat for f,stat in self.function_stats.items()} }, \n'
            f'          class_stats={ {c.signature: stat for c,stat in self.class_stats.items()} })\n'
        )

    ###################
    # Abstract methods
    # - Methods written without implementation, that
    #    must be overridden in the derived class!
    ###################
    @staticmethod
    @abstractmethod
    def name():
        """The name the stat will be registered as."""
        pass

    @abstractmethod
    def compute(self):
        """Computes the stat. Modifies `module_stats`, `function_stats`, etc."""
        pass


# Example 1: Module stat
class NumModuleLines(Statistic):
    """Computes the number of lines per module."""
    @staticmethod
    def name():
        """The name the stat will be registered as."""
        return 'NumModuleLines'

    def compute(self):
        """Computes the stat. Modifies `module_stats`, `function_stats`, etc."""
        # Add a stat to the overall module
        num_module_lines = len(self.parsed_file.lines)
        self.module_stats += [f'**Num Module Lines:** {num_module_lines}']


# Example 2: Function stats
class NumFuncLines(Statistic):
    """Computes the number of lines per function."""
    @staticmethod
    def name():
        """The name the stat will be registered as."""
        return 'NumFuncLines'

    def compute(self):
        """Computes the stat. Modifies `module_stats`, `function_stats`, etc."""
        # Add stats to each individual function
        for func_block in self.parsed_file.functions:
            self.function_stats[func_block] += [
                f'**Num Function Lines:** {len(func_block)}'
            ]
            logger.info(f'Length of the function blocks is {len(func_block)}')


# Example 3: Method stats
class NumMethodLines(Statistic):
    """Computes the number of lines per method."""
    @staticmethod
    def name():
        """The name the stat will be registered as."""
        return 'NumMethodLines'

    def compute(self):
        """Computes the stat. Modifies `module_stats`, `function_stats`, etc."""
        # Example of adding stats to each method
        # For each class ...
        for class_block in self.parsed_file.classes:
            # For each method in the class ...
            for method_block in self.parsed_file.methods[class_block]:
                self.function_stats[method_block] += [
                    f'**Num Method Lines:** {len(method_block)}'
                ]


class NumClassLines(Statistic):
    """Adds the statistics "Num Class Lines" and "Num Methods" to each class."""
    def name():
        return 'NumClassLines'

    def compute(self):
        # Adds stats to each individual class
        #  (nearly identical to NumFuncLines)
        for class_block in self.parsed_file.classes:
            self.class_stats[class_block] += [
                f'**Num Class Lines:** {len(class_block)}']

            self.class_stats[class_block] += [
                f'**Num Methods:** {len(self.parsed_file.methods[class_block])}']


class WarnNoDocstring(Statistic):

    VALID_DOCSTRINGS = ['"""', '"', "'", "'''"]
    NO_DOCSTRING_WARNING = f'**WARNING:** Missing docstring.'

    @staticmethod
    def name():
        return 'WarnNoDocstring'

    @staticmethod
    def has_docstring(method_lines):
        """Returns True if the method has a docstring on the second line."""
        # Assume docstring is on the line following the signature
        line = method_lines[1].lstrip()

        return any(line.startswith(s) for s in WarnNoDocstring.VALID_DOCSTRINGS)

    def add_docstring_warning(self, func_block):
        """Add 'no docstring' warning if no docstring exists."""
        if not self.has_docstring(func_block.lines):
            self.function_stats[func_block] += [
                WarnNoDocstring.NO_DOCSTRING_WARNING]

    def compute(self):
        """Add 'no docstring' warning for each function and method."""
        # Add function warnings
        for func_block in self.parsed_file.functions:
            self.add_docstring_warning(func_block)

        # Add method warnings
        for class_block in self.parsed_file.classes:
            # For each method in each class ...
            for method_block in self.parsed_file.methods[class_block]:
                self.add_docstring_warning(method_block)


class DunderMethodPythonPackage(Statistic):
    """Compute number of non python files in a package"""
    @staticmethod
    def name():
        """The name the stat will be registered as."""
        return 'NumNonPythonFile'

    def compute(self):
        """Computes the number of non python files per package"""
        dunderMethod = 0

        if self.parsed_file.filename.startswith('__'):
            dunderMethod += 1
        self.package_stats += [f'**dunder method in the package:** {dunderMethod}']