# __main__.py
#
# This file is run when a user runs:
# > python -m pystats
#
# Note this code was previously in pystats.py
#  inside `if __name__ == '__main__':`

import sys

from .pystats import PyStatsApp

args = PyStatsApp.parse_args(sys.argv[1:])
app = PyStatsApp(args.verbose)

app.run(args.input,
        filename_base=args.output,
        stat_names=args.stats,
        report_names=args.reports)

print('DONE.')