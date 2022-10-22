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
# ['Logger', 'PackageContext', 'PyStatsApp', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'app', 'config', 'context', 'parsed_file', 'report', 'statistic', 'utils']
# >>> pystats.PackageContext
# <class 'pystats.context.package_context.PackageContext'>

from pystats.app.pystats_app      import PyStatsApp