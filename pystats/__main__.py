'''
This file is run when a user runs:
> python -m pystats

Note this code was previously in pystats.py
 inside `if __name__ == '__main__':`
'''

import sys

# DEBUGGING
from app.pystats_app import PyStatsApp, PackageContext
from utils.logging.logger import Logger

# COMMANDLINE
# from pystats.app.pystats_app      import PyStatsApp
# from pystats.utils.logging.logger import Logger

logger = Logger(__name__).logger

def main():
    args = PackageContext.parse_args(sys.argv[1:])
    logger.info(f'''Parsing arguments from command line. INPUT : {args.input}, STATS: {args.stats}, REPORTS: {args.reports}, OUTPUT FILENAME: {args.output_filename}, VERBOSE: {args.verbose}''')
    app = PyStatsApp(args.verbose)
    # print(args.input)
    app.run(
        args.input,
        filename_base=args.output_filename,
        stat_names=args.stats,
        report_names=args.reports
    )
    logger.info(f'Successfully finished the job in {__name__}')


if __name__ == "__main__":
    main()