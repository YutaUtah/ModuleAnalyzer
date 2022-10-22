# This file is run when `import pystats` (the package) is run.
# The following imports make accessible under `pystats`:
#    - each of our classes, and
#    - `report` and `statistic`
#
# For example, given this __init__.py file, a user could run:
#  >> import pystats
#  >> pystats.PyStatsApp           # Valid because `PyStatsApp` is imported below
#  >> pystats.statistic.Statistic  # Valid because `statistic` is imported below
