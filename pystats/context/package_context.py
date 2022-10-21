import os
import sys

# COMMANDLINE
# from pystats.parsed_file          import ParsedFile
# from pystats.statistic            import NumModuleLines, NumFuncLines, NumMethodLines, NumClassLines, WarnNoDocstring, DunderMethodPythonPackage
# from pystats.report               import MarkdownReport
# from pystats.utils.logging.logger import Logger
# from pystats.utils.args_parser    import add_parser_options

# DEBUG
from parsed_file          import ParsedFile
from report               import MarkdownReport
from utils.logging.logger import Logger
from utils.args_parser    import add_parser_options
from statistic            import (
    NumModuleLines,
    NumFuncLines,
    NumMethodLines,
    NumClassLines,
    WarnNoDocstring,
    DunderMethodPythonPackage
)

logger = Logger(__name__).logger

class PackageContext:

    AVAILABLE_STATS = [
        NumModuleLines,
        NumFuncLines,
        NumMethodLines,
        NumClassLines,
        WarnNoDocstring,
        DunderMethodPythonPackage,
    ]

    AVAILABLE_REPORTS = [
        MarkdownReport,
    ]

    PACKAGE_STATS = [
        DunderMethodPythonPackage,
    ]
    PACKAGE_BASE_DIR = os.path.dirname(sys.modules['__main__'].__file__)

    @staticmethod
    def is_package(python_filenames):
        return len(python_filenames) and not python_filenames[0].endswith('.py')

    @staticmethod
    def get_package_depth(root):
        return root.count(os.path.sep) - PackageContext.PACKAGE_BASE_DIR.count(os.path.sep)


    @staticmethod
    def get_abs_path_python_filenames(python_filenames):
        # TODO: better way to write
        # TODO: this isn't robust 'User/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/app/statistic.py'
        return [os.path.join(PackageContext.PACKAGE_BASE_DIR, python_filename) for python_filename in python_filenames ]


    @staticmethod
    def parse_args(arguments):
        '''Given a list of command-line arguments, returns them parsed.'''
        parser = add_parser_options(PackageContext)
        return parser.parse_args(arguments)


    @staticmethod
    def get_lines(filename):
        '''Returns the lines in `filename` stripped of terminal.'''
        lines = []
        # todo:
        # filename = '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/statistic.py'
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]

        return lines


    @staticmethod
    def parse_modules(filenames, verbose=False):
        '''
        Parses each of `filenames`, which refer to Python modules.

        Returns:
            A list of `ParsedFile` objects, each corresponding to a filename.
        '''
        modules = []

        # Parse each module
        for filename in filenames:
            filename = filename.strip()
            if filename:
                lines = []

                if verbose:
                    logger.info(f'Parsing "{filename}"')

                # Read lines from the file
                try:
                    lines = PackageContext.get_lines(filename)
                except Exception as error:
                    if verbose:
                        modulename = filename.split('/')[-1]
                        logger.error(f'ERROR OPENING {modulename}')
                    raise error

                # Parse the lines
                if lines:
                    modules.append(ParsedFile(filename, lines))
                    if verbose:
                        logger.info(f'Finished parsing {filename}')

        return modules
