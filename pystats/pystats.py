"""
pystats.py

A command-line interface to `pystats`.
"""

import os
import sys
import argparse

from collections import defaultdict

# In a package, the working directory is no longer the package directory,
#   so `from parsed_file ...` and `import statistic` will no longer work:

# from parsed_file import ParsedFile
# import statistic
# import report

# In a package, we can write imports either relative to the package `pystats`,
#   or relative to this file using `.`.
from parsed_file import ParsedFile
import statistic
import report

# Default output filename (without a file extension)
OUTPUT_FILENAME_BASE = 'out'

class PyStatsApp:
    """
    A command-line interface to `pystats`.
    """
    ########################
    # Class Variables
    ########################

    AVAILABLE_STATS = [
        statistic.NumModuleLines,
        statistic.NumFuncLines,
        statistic.NumMethodLines,
        statistic.NumClassLines,
        statistic.WarnNoDocstring,
        statistic.dunderMethodPythonPackage,
    ]

    AVAILABLE_REPORTS = [
        report.MarkdownReport,
    ]

    PACKAGE_STATS = [
        statistic.dunderMethodPythonPackage,
    ]
    ########################
    # Static Methods
    ########################

    # For more information about `argparse`, see:
    #    https://docs.python.org/3/howto/argparse.html
    @staticmethod
    def parse_args(arguments):
        """Given a list of command-line arguments, returns them parsed."""
        parser = argparse.ArgumentParser()

        # One or more filenames are required.
        parser.add_argument('input',
                            action='store',
                            nargs='+',
                            metavar='FILENAME',
                            help='the input Python file(s)')

        # Specifying one or more stats is optional. By default, will run all stats.
        parser.add_argument(
            '-s',
            '--stats',
            action='store',
            default=[],
            nargs='*',
            choices=[s.name() for s in PyStatsApp.AVAILABLE_STATS],
            help=
            'include only the specified one or more stats (default: all stats)'
        )

        # Specifying one or more reports is optional. By default, will generate a Markdown report.
        parser.add_argument(
            '-r',
            '--reports',
            action='store',
            default=[],
            nargs='*',
            choices=[r.name() for r in PyStatsApp.AVAILABLE_REPORTS],
            help='generate only the specified one or more reports')

        # Specifying the output filename.
        parser.add_argument(
            '-o',
            '--output_filename',
            action='store',
            default=['out'],
            nargs='*',
            help='enter the output filename')

        # For testing/debugging, can generate additional output based on this flag.
        parser.add_argument("--silent",
                            action="store_false",
                            dest="verbose",
                            default=True,
                            help='silence output')

        args = parser.parse_args(arguments)

        return args


    @staticmethod
    def get_lines(filename):
        """Returns the lines in `filename` stripped of terminal \n."""
        lines = []
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
                    print(f'- Parsing "{filename}" ... ', end='')

                # Read lines from the file
                try:
                    lines = PyStatsApp.get_lines(filename)
                except:
                    if verbose:
                        print('ERROR OPENING - Skipped.')

                # Parse the lines
                if lines:
                    modules.append(ParsedFile(filename, lines))
                    if verbose:
                        print('OK')

        return modules

    ########################
    # Public Methods
    ########################

    def __init__(self, verbose=False):
        """Initializes a new `PyStatsApp`."""
        self.modules = []
        self.stats = defaultdict(list)
        self.verbose = verbose

    def __repr__(self):
        return (
            f'PyStatsApp(num_modules={len(self.modules)},\n'
            f'           num_stats={len(self.stats)},\n'
            f'           verbose={self.verbose})\n'
        )

    def write_report(self,
                     ComputedReport,
                     stats,
                     filename_base=OUTPUT_FILENAME_BASE):
        """Generates a report of type `ComputedReport` and writes it to disk.

        Args:
        - ComputedReport: A class that inherits from `Report`.
        - stats: A dict mapping `ParsedFile`s to a list of `Stat`s generated from it.

        Returns:
        - None (Writes the report file to disk.)
        """
        report = ComputedReport(self.modules, stats)

        out_filename = filename_base + report.file_extension()

        # Write the report to disk.
        try:
            report.write(filename_base)
            if self.verbose:
                print(f'- Saved {report.name()} to "{out_filename}".')
        except:
            if self.verbose:
                print(f'- Error saving {report.name()} to "{out_filename}".')

    def run(self,
            python_filenames,
            filename_base=OUTPUT_FILENAME_BASE,
            stat_names=[],
            report_names=[],
            package_stats_names=[]):
        """
        Parses each Python file/module, computes each `stats` statistic per module,
         then generates each of the `reports`.
        """

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

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        given_package = python_filenames[0]

        # scenario when its package
        if len(python_filenames) == 1 and not python_filenames[0].endswith('.py'):
            package_dir = os.path.join(root_dir, given_package)
            current_dir_filenames = [filename for root, dirs, filename in os.walk(package_dir)][0]
            python_filenames = [filename for filename in current_dir_filenames if filename.endswith('.py')]

        # 1. PARSE MODULES
        self.modules = PyStatsApp.parse_modules(python_filenames,
                                                verbose=self.verbose)

        if self.verbose:
            print(f'Parsed {len(self.modules)} Python module(s).\n')

        # 2. COMPUTE STATS
        # Maps each `ParsedFile` to a list of `Statistic`s.
        self.stats = defaultdict(list)
        for module in self.modules:
            for ComputedStat in requested_stats:
                self.stats[module].append(ComputedStat(module))

        # package directory list for Package statistics
        if package_stats_names:
            self.package_stats = defaultdict(list)
            for stats in requested_package_name:
                self.pkgstats['PackageStats'].append(stats(self.dir_list))

        # 3. GENERATE REPORTS
        for ComputedReport in requested_reports:
            self.write_report(ComputedReport,
                              self.stats,
                              filename_base=filename_base)


if __name__ == '__main__':

    args = PyStatsApp.parse_args(sys.argv[1:])
    app = PyStatsApp(args.verbose)
    # print(args.input)
    # print(args.output_filename[0])
    # print(args.stats)
    # print(args.reports)
    app.run(args.input,
            filename_base=args.output_filename[0],
            stat_names=args.stats,
            report_names=args.reports)
    print('DONE')