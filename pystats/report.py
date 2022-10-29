"""
report.py

Generates and writes to disk a report from `ParsedFile`s and `Statistic`s.

A report is structured as follows:

<header>
<module 1 + stats>
    <class 1 + stats>
        - <method 1 + stats>
        - ...
    - ...
    - <function 1 + stats>
    - ...
---
...
<footer>
"""
from abc import ABCMeta, abstractmethod


class Report(metaclass=ABCMeta):
    def __init__(self, parsed_files, statistics):
        """Initialize a new report.
        Args:
            parsed_files: A list of `ParsedFile` objects
            statistics: A dict of `ParsedFile` keys, with a list of `Statistic`s for each.
        """
        self.parsed_files = parsed_files
        self.statistics = statistics

    def write(self, filename_base):
        """
        Renders the report and writes it to disk as the file
           `filename_base` followed by the report's extension.

        For example, file_base='out' may write 'out.md' for MarkdownReport.
        """
        out_file = filename_base + self.file_extension()
        report_output = self.render()

        with open(out_file, 'w') as file:
            file.write(report_output)

    ###################
    # Abstract methods
    # - Methods written without implementation, that
    #    must be overridden in the derived class!
    ###################
    @staticmethod
    @abstractmethod
    def name():
        """Returns the name the report will be registered as."""
        pass

    @staticmethod
    @abstractmethod
    def file_extension():
        """Returns the file extension of the report."""
        pass

    @abstractmethod
    def render(self):
        """Returns the report as a string."""
        pass


class MarkdownReport(Report):
    """Generates a MarkDown report."""
    @staticmethod
    def name():
        """Returns the name the report will be registered as."""
        return 'MarkdownReport'

    @staticmethod
    def file_extension():
        """Returns the file extension of the report."""
        return '.md'

    def render(self):
        """Returns the report as a string."""
        markdown_lines = ['# `pystats` Report']
        markdown_lines += [f'**Num Modules:** {len(self.parsed_files)}']
        # TODO: include _printTree maybe not a great idea to break encapsulation..... check this module L30

        # For each module ...
        for module in self.parsed_files:
            stats = self.statistics[module]

            # Start of module
            markdown_lines += [f'\n---\n']

            # MODULE
            markdown_lines += [f'## module: {module.name}']
            # Module-level stats
            for stat in stats:
                markdown_lines += [f'- {s}' for s in stat.module_stats]

            # For each class ...
            markdown_lines += [f'### Classes']
            if not module.classes:
                markdown_lines += [f'- No Class']

            for class_block in module.classes:
                # CLASS
                markdown_lines += [f'#### `class {class_block.signature}`']
                # Class-level stats
                for stat in stats:
                    if class_block in stat.class_stats:
                        markdown_lines += [
                            f'- {s}' for s in stat.class_stats[class_block]
                        ]

                # METHODS
                markdown_lines += [f'**Methods.**']
                for method_block in sorted(module.methods[class_block],
                                           key=lambda mb: mb.signature):
                    markdown_lines += [f'- `{method_block.signature}`']
                    # Method-level stats
                    for stat in stats:
                        if method_block in stat.function_stats:
                            markdown_lines += [
                                f'    - {s}'
                                for s in stat.function_stats[method_block]
                            ]

            # FUNCTIONS
            markdown_lines += [f'### Functions']
            if not module.functions:
                markdown_lines += [f'- No Function']

            for func_block in sorted(module.functions,
                                     key=lambda fb: fb.signature):
                markdown_lines += [f'- `{func_block.signature}`']
                # Function-level stats
                for stat in stats:
                    if func_block in stat.function_stats:
                        markdown_lines += [
                            f'    - {s}'
                            for s in stat.function_stats[func_block]
                        ]

        return '\n'.join(markdown_lines)
