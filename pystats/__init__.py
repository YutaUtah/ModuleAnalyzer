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


paths = PyStatsApp(verbose=True).getPaths(['pystats'])

import os
for l in paths:
    temp_dir_collection = set()
    os.makedirs('./pystats_report/', exist_ok=True)
    for path in l[1:]:
        report_name = './' + str(path.relative_to(os.getcwd())).split('/')[0] + '_report'
        sub_dir_path = '/'.join(str(path.relative_to(os.getcwd())).split('/')[1:-1])
        sub_file_path = '/'.join(str(path.relative_to(os.getcwd())).split('/')[1:]) if len(str(path.relative_to(os.getcwd())).split('/')) != 2 else ''
        report_path = os.path.join(os.getcwd(), report_name)
        if sub_dir_path not in temp_dir_collection:
            os.makedirs(os.path.join(report_name, sub_dir_path), exist_ok=True)
            temp_dir_collection.add(sub_dir_path)
        if len(sub_file_path) == 0:
            sub_file_path = str(path).split('/')[-1]
        target_md_path = os.path.join(report_name, sub_file_path).replace('.py', '.md')
        with open(target_md_path, mode='w') as f:
            f.write('hello!')
# PyStatsApp(verbose=True).printTree(['pystats'])