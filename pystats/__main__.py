# __main__.py
#
# This file is run when a user runs:
# > python -m pystats
#
# Note this code was previously in pystats.py
#  inside `if __name__ == '__main__':`

import sys
import logging

# DEBUGGING needs to do "from pystats_app import PyStatsApp"
# from command line, needs to do "from .pystats_app import PyStatsApp"
from .pystats_app import PyStatsApp

logging.basicConfig(
    format='%(levelname)s: %(asctime)s [ %(filename)s line %(lineno)d] %(message)s', datefmt='%I:%M:%S %p %m/%d/%Y', level=logging.DEBUG, stream=sys.stdout
)

logger = logging.getLogger(__name__)

args = PyStatsApp.parse_args(sys.argv[1:])
logging.info(f'Parsing arguments from command line. INPUT : {args.input}, STATS: {args.stats}, REPORTS: {args.reports}, OUTPUT FILENAME: {args.output_filename}, VERBOSE: {args.verbose}')
app = PyStatsApp(args.verbose)

app.run(
    args.input,
    filename_base=args.output_filename,
    stat_names=args.stats,
    report_names=args.reports
)

logger.info(f'Successfully finished the job in {__name__}')