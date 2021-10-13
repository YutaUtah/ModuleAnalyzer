"""
pystats.py

A command-line interface to `pystats`.
"""

import sys
import argparse

from collections import defaultdict

from parsed_file import ParsedFile
import statistic
import report

# Default output filename (without a file extension)
OUTPUT_FILENAME_BASE = 'out'

class PyStatsApp:
    """
    A command-line interface to `pystats`
    """
    ##########################
    # class variable
    ##########################

    AVAILABLE_STATS = [
        statistic.NumModuleLines,
        statistic.NumFuncLines,
        statistic.NumMethodLines,
    ]

    AVAILABLE_REPORTS = [
        report.MarkdownReport,
    ]

    ##########################
    # static Methods
    ##########################
    @staticmethod
    def parse_args(arguments):
        """Given a list of command-line arguments, returns them parsed."""
    parser = argparse.ArgumentParser()

    # PROBLEM 4: Add a -o, --output argument for specifying an output file.

    #todo:


    #PROBLEM 1:
    @staticmethod
    def get_lines(filename):
        """Returns the lines in `filename` stripped of terminal \n."""
        with open(filename, 'r') as file:
            return [line.replace('\n', '') for line in file]


    @staticmethod
    def parse_modules(filenames, verbose=False):
        """
        Parses each of `filenames`, which refer to Python modules.

        :returns
            A list of `ParsedFile` objects, each corresponding to a filename
        """
        modules = []

        # Parse each module
        for filename in filenames:
            filename = filename.strip()
            if filename:
                lines = []

                if verbose:
                    print(f' - Parsing "{filename}" ... ', end='')

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


    ##########################
    # Public Methods
    ##########################

    def __init__(self, verbose=False):
        self.modules = []
        self.stats = defaultdict(list)
        self.verbose = verbose

    def __repr__(self):
        return (
            f'PystatsApp(num_modules={len(self.modules)},\n'
            f'          (num_stats={len(self.stats)},\n'
            f'          (verbose={self.verbose},\n'
        )

    def write_report(self,
                     ComputedReport,
                     stats):

        report = ComputedReport(self.modules, stats)

        filename_base = OUTPUT_FILENAME_BASE
        output_filename = filename_base + report.file_extension()

        # write the report to disk
        try:
            report.write(filename_base)
            if self.verbose:
                print(f' - Saved {report.name()} to "{output_filename}".')

        except:
            if self.verbose:
                print(f' - Error Saving {report.name()} to "{output_filename}".')

    def run(self,
            python_filenames,
            filename_base=OUTPUT_FILENAME_BASE,
            stat_names=[],
            report_names=[]):

        # Map each
        requested_stats = PyStatsApp.AVAILABLE_STATS
        if stat_names:
            requested_stats = [
                s for s in PyStatsApp.AVAILABLE_STATS if s.name() in stat_names
            ]

        requested_reports= PyStatsApp.AVAILABLE_REPORTS
        if report_names:
            requested_reports = [
                r for r in PyStatsApp.AVAILABLE_REPORTS
                if r.name() in report_names
            ]

        # 1. PARSE MODULES
        self.modules = PyStatsApp.parse_modules(python_filenames,
                                                verbose=self.verbose)

        if self.verbose:
            print(f'Parsed {len(self.modules)} Python modules(s).\n')

        # 2. COMPUTE STATS
        # Maps each `parsedFile` to a list of `Statistic`s.
        self.stats = defaultdict(list)
        for module in self.modules:
            for ComputedStat in requested_stats:
                self.stats[module].append(ComputedStat(module))

        # 3. GENERATE REPORTS
        for ComputedReport in requested_reports:
            self.write_report(ComputedReport,
                              self.stats)


if __name__ == '__main__':
    args = PyStatsApp.parse_args(sys.argv[1:])
    app = PyStatsApp(args.verbose)

    app.run(args.input,
            stats_names=args.stats,
            report_names=args.reports)

    print('done')