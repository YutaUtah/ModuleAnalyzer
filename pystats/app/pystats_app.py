'''
A command-line interface to `pystats`.

In a package, the working directory is no longer the package directory,
  so `from parsed_file ...` and `import statistic` will no longer work:
In a package, we can write imports either relative to the package `pystats`,
  or relative to this file using `.`.
'''

import os
from collections import defaultdict

# COMMANDLINE
from pystats.config.config        import OUTPUT_FILENAME_BASE
from pystats.parsed_file          import ParsedFile
from pystats.statistic            import NumModuleLines, NumFuncLines, NumMethodLines, NumClassLines, WarnNoDocstring, DunderMethodPythonPackage
from pystats.report               import MarkdownReport
from pystats.utils.logging.logger import Logger
from pystats.utils.args_parser    import add_parser_options

# DEBUG
# from pystats.config               import OUTPUT_FILENAME_BASE
# from parsed_file          import ParsedFile
# from statistic            import NumModuleLines, NumFuncLines, NumMethodLines, NumClassLines, WarnNoDocstring, DunderMethodPythonPackage
# from report               import MarkdownReport
# from utils.logging.logger import Logger
# from utils.args_parser    import add_parser_options

logger = Logger(__file__)

class PyStatsApp:
    '''
    A command-line interface to `pystats`.
    '''
    ########################
    # Class Variables
    ########################

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
    ########################
    # Static Methods
    ########################

    @staticmethod
    def parse_args(arguments):
        '''Given a list of command-line arguments, returns them parsed.'''
        parser = add_parser_options(PyStatsApp)
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
        """Parses each of `filenames`, which refer to Python modules.

        Returns:
            A list of `ParsedFile` objects, each corresponding to a filename.
        """
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
                    lines = PyStatsApp.get_lines(filename)
                except:
                    if verbose:
                        #todo: exception more restrict rule
                        modulename = filename.split('/')[-1]
                        logger.error(f'ERROR OPENING {modulename} Skipping.')

                # Parse the lines
                if lines:
                    modules.append(ParsedFile(filename, lines))
                    if verbose:
                        logger.info(f'Finished parsing {filename}')

        return modules

    @staticmethod
    def is_package(python_filenames):
        return len(python_filenames) == 1 and not python_filenames[0].endswith('.py')

    ########################
    # Public Methods
    ########################

    def __init__(self, verbose=False):
        """Initializes a new `PyStatsApp`."""
        self.modules = []
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.stats = defaultdict(list)
        self.verbose = verbose

    def __repr__(self):
        return (
            f'PyStatsApp(num_modules={len(self.modules)},\n'
            f'           num_stats={len(self.stats)},\n'
            f'           verbose={self.verbose})\n'
        )

    def get_abs_path_python_filenames(self, python_filenames):
        #todo: better way to write
        return [os.path.join(self.root_dir, python_filename) for python_filename in python_filenames ]

    def write_report(
        self,
        ComputedReport,
        stats,
        filename_base=OUTPUT_FILENAME_BASE
    ):
        '''
        Generates a report of type `ComputedReport` and writes it to disk.

        Args:
        - ComputedReport: A class that inherits from `Report`.
        - stats: A dict mapping `ParsedFile`s to a list of `Stat`s generated from it.

        Returns:
        - None (Writes the report file to disk.)
        '''
        report = ComputedReport(self.modules, stats)

        out_filename = filename_base + report.file_extension()

        # Write the report to disk.
        try:
            report.write(filename_base)
            if self.verbose:
                logger.info(f'Saved {report.name()} to "{out_filename}".')
        except:
            if self.verbose:
                logger.error(f'Error saving {report.name()} to "{out_filename}".')

    def run(self,
            python_filenames,
            filename_base=OUTPUT_FILENAME_BASE,
            stat_names=[],
            report_names=[],
            package_stats_names=[]):
        '''
        Parses each Python file/module, computes each `stats` statistic per module,
         then generates each of the `reports`.
        '''

        # Map each
        requested_stats = PyStatsApp.AVAILABLE_STATS
        if stat_names:
            requested_stats = [
                s for s in PyStatsApp.AVAILABLE_STATS if s.name() in stat_names
            ]

        requested_reports = PyStatsApp.AVAILABLE_REPORTS
        if report_names:
            requested_reports = [
                r for r in PyStatsApp.AVAILABLE_REPORTS
                if r.name() in report_names
            ]

        if package_stats_names:
            requested_package_name = [
                s for s in PyStatsApp.PACKAGE_STATS if s.name() in package_stats_names
            ]

        given_package = python_filenames[0]

        # scenario when its package
        if PyStatsApp.is_package(python_filenames):
            package_dir = os.path.join(self.root_dir, given_package)
            current_dir_filenames = [filename for root, dirs, filename in os.walk(package_dir)][0]
            python_filenames = [filename for filename in current_dir_filenames if filename.endswith('.py')]


        # 1. PARSE MODULES
        self.modules = PyStatsApp.parse_modules(
            filenames=self.get_abs_path_python_filenames(python_filenames),
            verbose=self.verbose
        )

        if self.verbose:
            logger.info(f'Parsed {len(self.modules)} Python module(s)')

        # 2. COMPUTE STATS
        # Maps each `ParsedFile` to a list of `Statistic`s.
        for module in self.modules:
            for ComputedStat in requested_stats:
                self.stats[module].append(ComputedStat(module))

        # package directory list for Package statistics
        if package_stats_names:
            for stats in requested_package_name:
                self.pkgstats['PackageStats'].append(stats(self.dir_list))

        # 3. GENERATE REPORTS
        for ComputedReport in requested_reports:
            self.write_report(
                ComputedReport,
                self.stats,
                filename_base=filename_base[0]
            )