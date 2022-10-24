# This file is run when `import pystats` (the package) is run.
# The following imports make accessible under `pystats`:
#    - each of our classes, and
#    - `report` and `statistic`
#
# For example, given this __init__.py file, a user could run:
#  >> import pystats
#  >> pystats.PyStatsApp           # Valid because `PyStatsApp` is imported below
#  >> pystats.statistic.Statistic  # Valid because `statistic` is imported below

from __future__ import annotations

# >> import pystats
# >>> pystats.PackageContext
# <class 'pystats.context.package_context.PackageContext'>
try:
    from pystats.app.pystats_app import PyStatsApp
except:
    from app.pystats_app         import PyStatsApp


# paths = PyStatsApp(verbose=True).getReports(packagename_path=['/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats', '/Users/yutahayashi/VisualStudioProjects/ModuleAnalyzer/pystats/utils'])

# PyStatsApp(verbose=True).getReports()