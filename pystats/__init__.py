# __init__.py
# 
# This file is run when `import pystats` (the package) is run.
# The following imports make accessible under `pystats`:
#    - each of our classes, and 
#    - `report` and `statistic`
#
# For example, given this __init__.py file, a user could run:
#  >> import pystats
#  >> pystats.PyStatsApp           # Valid because `PyStatsApp` is imported below
#  >> pystats.statistic.Statistic  # Valid because `statistic` is imported below

from pystats.pystats import PyStatsApp
from pystats.parsed_file import CodeBlock, ParsedFile

from pystats.report import Report
from pystats.statistic import Statistic

from . import report
from . import statistic
