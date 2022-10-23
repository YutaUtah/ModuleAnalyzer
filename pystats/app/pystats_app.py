'''
A command-line interface to `pystats`.

In a package, the working directory is no longer the package directory,
  so `from parsed_file ...` and `import statistic` will no longer work:
In a package, we can write imports either relative to the package `pystats`,
  or relative to this file using `.`.
'''

import os
from   collections import defaultdict

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

# With a criteria (skip hidden files)
def is_not_hidden(path):
    return not path.name.startswith(".")

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

        try:
            for python_package in python_packages:
                DisplayablePath.printTree(python_package)

        except (FileNotFoundError, TypeError):
            if not isinstance(python_packages, list):
                raise TypeError(f'type mismatch (python_packages): list is expected for {python_packages}')
            if PackageContext.is_package(python_packages):
                raise FileNotFoundError(f'not package: {python_package}')


    def getPaths(self, python_packages):
        '''
        Get the list of package paths that are displayed as absolute path

        EX)
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/__init__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/__main__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/app/__init__.py
        /Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/app/pystats_app.py
        '''

        file_hierarchy_list = []

        try:
            for python_package in python_packages:
                file_hierarchy_list.append(DisplayablePath.getPaths(python_package))

        except (FileNotFoundError, TypeError):
            if not isinstance(python_packages, list):
                raise TypeError(f'type mismatch (python_packages): list is expected for {python_packages}')
            if PackageContext.is_package(python_packages):
                raise FileNotFoundError(f'not package: {python_package}')


        return file_hierarchy_list


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

    def run(
        self,
        python_filenames,
        filename_base=OUTPUT_FILENAME_BASE,
        stat_names=[],
        report_names=[],
        package_stats_names=[]
    ):
        '''
        Parses each Python file/module, computes each `stats` statistic per module,
         then generates each of the `reports`.
        '''

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
            requested_package_name = [
                s for s in PackageContext.PACKAGE_STATS if s.name() in package_stats_names
            ]
        else:
            package_stats_names = PackageContext.PACKAGE_STATS


        # scenario when its package
        if PackageContext.is_package(python_filenames):
            package_layer = []
            for root, dirs, filename in os.walk(PackageContext.PACKAGE_BASE_DIR, topdown=False):
                if '/.git' in root or root.endswith('__pycache__'):
                    continue
                if '__pycache__' in dirs:
                    dirs.remove('__pycache__')
                filenames = [filename for filename in filename if not filename.endswith('.pyc')]
                package_layer_info = {
                    'root': root,
                    'dirs': dirs,
                    'filenames': filenames,
                    'package_depth': PackageContext.get_package_depth(root),
                }
                # logger.info(f'Root Dir: {root}, Directory: {dirs}, File Names: {filenames}, Package Depth: {PackageContext.get_package_depth(root)}')
                package_layer.append(package_layer_info)


        # 1. PARSE MODULES
        self.modules = PackageContext.parse_modules(
            filenames=PackageContext.get_abs_path_python_filenames(python_filenames),
            verbose=self.verbose
        )
        #TODO:
        logger.info(f'Parsed File Info: {self.modules}')

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