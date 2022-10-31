'''
A command-line interface to `pystats`.

In a package, the working directory is no longer the package directory,
  so `from parsed_file ...` and `import statistic` will no longer work:
In a package, we can write imports either relative to the package `pystats`,
  or relative to this file using `.`.
'''

import os
from collections import defaultdict
from functools import wraps
from plistlib import InvalidFileException

try:
# DEBUG
    from config.config               import OUTPUT_FILENAME_BASE
    from context.package_context     import PackageContext
    from utils.format_tree           import DisplayablePath
    from utils.logging.logger        import Logger
except:
# COMMANDLINE
    from pystats.config.config        import OUTPUT_FILENAME_BASE
    from pystats.utils.logging.logger import Logger
    from pystats.context.package_context      import PackageContext
    from pystats.utils.format_tree           import DisplayablePath


logger = Logger(__name__).logger


class PyStatsApp:
    '''
    A command-line interface to `pystats`.
    '''
    def __init__(self, verbose=False):
        '''Initializes a new `PyStatsApp`.'''
        self.modules = []
        self.stats = defaultdict(list)
        self.verbose = verbose


    def __repr__(self):
        return (
            f"<class '{__name__}'>\n"
            f'PyStatsApp(num_modules={len(self.modules)},\n'
            f'           num_stats={len(self.stats)},\n'
            f'           verbose={self.verbose})\n'
        )


    def _print_header(func):
        @wraps(func)
        def inner(self, python_packages):
            print('================================================================')
            print('============             TREE STRUCTURE             ============')
            print('================================================================\n')
            func(self, python_packages)
            print('\n================================================================')

        return inner


    @_print_header
    def printTree(self, python_packages):
        '''
        Print the tree structure of specified python_packages.

        Argument value you pass must be a list (str type not accepted)

        EX)
        pystats/
        ├── __init__.py
        ├── __main__.py
        └── app/
            ├── __init__.py
            └── pystats_app.py
        '''
        self._printTree(python_packages)


    def getPaths(self, python_package):
        '''
        Get the list of package paths that are displayed as absolute path

        EX)
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/__init__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/__main__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/app/__init__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/app/pystats_app.py
        '''
        if not isinstance(python_package, str):
            raise TypeError(f'type mismatch (python_package): string is expected for {python_package}')

        try:
            return DisplayablePath.getPaths(python_package)

        except:
            raise FileNotFoundError(f'Unable to get package paths: {python_package}')


    def getMarkdownPath(self, pakcage):
        try:
            return DisplayablePath.getMarkdownPath(pakcage)
        except:
            raise FileNotFoundError(f'Unable to get package paths: {pakcage}')


    def getReports(self, packagename_path=[], target_creation_path=None):
        '''
        Generates reports for given packages as a markdown format. Note that non-python file report will not be generated

        Args:
        - packagename_path: A list of targetd "absolute" package directory paths i.e. Mac starts from '/Users/yutahayashi/... Cannot be empty.
        - target_creation_path: Absolute path that you wish to store your generated markdown report. If you leave it empty, your terminal/console path will be the root directory.

        Returns:
        - None (Writes the report file to disk.)
        '''

        def already_exist(folder):
            return folder in existed_folders

        if isinstance(packagename_path, list):
            if len(packagename_path) == 0:
                raise FileNotFoundError('package path is absolute and mandatory field')

        else:
            raise TypeError('Package absolute path needs to be in list: str object must be encolsed with []')

        try:
            package_file_paths = self.getPaths(packagename_path)
        except Exception as e:
            raise e.message

        # if not target_creation_path:
        target_creation_path = target_creation_path or os.getcwd()

        for i, paths in enumerate(package_file_paths):
            existed_folders = set()
            report_folder_base = os.path.join(target_creation_path, os.path.basename(packagename_path[i]) + '_report')

            # Create the generate report base folder i.e. package_name + _report
            os.makedirs(report_folder_base, exist_ok=True)

            for path in paths[1:]:

                target_folder = str(path.parent)
                absolute_module_path = os.path.join(report_folder_base, os.path.relpath(path, packagename_path[i]))

                # if TARGET_FOLDER not in existed_folders:
                if not already_exist(target_folder):
                    os.makedirs(
                        os.path.join(
                            report_folder_base,
                            os.path.relpath(target_folder, packagename_path[i])
                        ),
                    exist_ok=True
                    )
                    existed_folders.add(target_folder)

                if not absolute_module_path.endswith('.py'):
                    raise InvalidFileException(
                        'Currently only Python extention is supported. Apologies for the inconvenience...'
                    )

                absolute_report_path = absolute_module_path.replace('.py', '.md')

                with open(absolute_report_path, mode='w') as f:
                    f.write('hello!')


    def write_report(
        self,
        ComputedReport,
        stats,
        tree,
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
        report = ComputedReport(self.modules, stats, tree)

        out_filename = filename_base + report.file_extension()

        # Write the report to disk.
        try:
            report.write(filename_base)
            if self.verbose:
                logger.info(f'Saved {report.name()} to "{out_filename}".')
        except:
            if self.verbose:
                logger.error(f'Error saving {report.name()} to "{out_filename}".')


    def _printTree(self, python_packages):
        if isinstance(python_packages, list):
            if all(map(lambda x: isinstance(x, str), python_packages)):
                try:
                    for python_package in python_packages:
                        DisplayablePath.printTree(python_package)
                    return

                except FileNotFoundError:
                    raise FileNotFoundError(
                        f'not package: {python_package}: please make sure if the path is appropriate'
                    )
            else:
                raise TypeError(
                    f'type mismatch (one of the elements in python_packages): all elements must be str. Check {python_packages}'
                )

        raise TypeError(
            f'type mismatch (python_packages): list is expected for your input: {python_packages}'
            )


    def run(
        self,
        pypackage_paths,
        filename_base=OUTPUT_FILENAME_BASE,
        stat_names=[],
        report_names=[],
        package_stats_names=[]
    ):
        '''
        Parses each Python file/module, computes each `stats` statistic per module,
        then generates each of the `reports`.
        '''
        #TODO: error handling
        self.tree_markdown = self.getMarkdownPath(os.path.relpath(pypackage_paths, os.getcwd()))

        # Map each
        if stat_names:
            requested_stats = [
                s for s in PackageContext.AVAILABLE_STATS if s.name() in stat_names
            ]
        else:
            requested_stats = PackageContext.AVAILABLE_STATS

        if report_names:
            requested_reports = [
                r for r in PackageContext.AVAILABLE_REPORTS
                if r.name() in report_names
            ]
        else:
            requested_reports = PackageContext.AVAILABLE_REPORTS

        if package_stats_names:
            requested_stats_name = [
                s for s in PackageContext.PACKAGE_STATS if s.name() in package_stats_names
            ]
        else:
            requested_stats_name = PackageContext.PACKAGE_STATS

        # scenario when its package
        if PackageContext.is_package(pypackage_paths):
            module_paths = self.getPaths(pypackage_paths)

        # "Parse Module": store in ParsedFile class
        # module_paths is a collection of filenames: [file1, file2...]
        self.modules = PackageContext.parse_modules(
            filenames=module_paths,
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
        # package_stats_name inherits from the args
        if package_stats_names:
            for stats in requested_stats_name:
                self.pkgstats['PackageStats'].append(stats(self.dir_list))

        # Generate Reports
        for ComputedReport in requested_reports:
            logger.info(f'parsing {ComputedReport.name()}')
            # include printTree from format_tree func
            self.write_report(
                ComputedReport,
                self.stats,
                self.tree_markdown,
                filename_base=filename_base
            )