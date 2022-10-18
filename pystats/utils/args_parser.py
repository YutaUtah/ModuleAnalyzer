import argparse

def add_parser_options(app):

    parser = argparse.ArgumentParser()

    # One or more filenames are required.
    parser.add_argument(
        'input',
        action='store',
        nargs='+',
        metavar='FILENAME',
        help='the input Python file(s)'
    )

    # Specifying one or more stats is optional. By default, will run all stats.
    parser.add_argument(
        '-s',
        '--stats',
        action='store',
        default=[],
        nargs='*',
        choices=[s.name() for s in app.AVAILABLE_STATS],
        help=
        'include only the specified one or more stats (default: all stats)'
    )

    # Specifying one or more reports is optional. By default, will generate a Markdown report.
    parser.add_argument(
        '-r',
        '--reports',
        action='store',
        default=[],
        nargs='*',
        choices=[r.name() for r in app.AVAILABLE_REPORTS],
        help='generate only the specified one or more reports'
    )

    # Specifying the output filename.
    parser.add_argument(
        '-o',
        '--output_filename',
        action='store',
        default=['out'],
        nargs='*',
        help='enter the output filename'
    )

    # For testing/debugging, can generate additional output based on this flag.
    parser.add_argument(
        "--silent",
        action="store_false",
        dest="verbose",
        default=True,
        help='silence output'
    )

    return parser
