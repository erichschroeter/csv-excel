
import argparse
import logging
import os
import textwrap

from csv_excel.csv_excel import csv2xl, validate, xl2csv


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


class App:
    def __init__(self) -> None:
        self.args = None
        self.parser = argparse.ArgumentParser(
            description=textwrap.dedent('''\
                A commandline utility to manage an Excel file with multiple worksheets while keeping data in CSV files for better Git support.
                '''),
            formatter_class=RawTextArgumentDefaultsHelpFormatter)
        self.parser.add_argument('-v', '--verbosity',
                                 choices=['critical', 'error', 'warning', 'info', 'debug'],
                                 default='info',
                                 help='Set the logging verbosity level.')
        self.parser.add_argument('-c', '--config',
                                 help='A YAML configuration file.')

        self.subparsers = self.parser.add_subparsers(dest='command')
        csv2xl_parser = self.subparsers.add_parser('csv2xl',
                                                   help='Generate or update an Excel file from multiple CSV files.',
                                                   formatter_class=RawTextArgumentDefaultsHelpFormatter)
        csv2xl_parser.add_argument('-o', '--output', default='output.xlsm', help='The output Excel file')
        csv2xl_parser.add_argument('csv_files', nargs='+', help='The CSV files to include in the Excel file')
        csv2xl_parser.set_defaults(func=csv2xl)
        xl2csv_parser = self.subparsers.add_parser('xl2csv',
                                                   help='Exports worksheets to CSV files.',
                                                   formatter_class=RawTextArgumentDefaultsHelpFormatter)
        xl2csv_parser.add_argument('-o', '--output_dir', help='The output Excel file')
        xl2csv_parser.add_argument('file', help='The Excel file')
        xl2csv_parser.set_defaults(func=xl2csv)
        validate_parser = self.subparsers.add_parser('validate',
                                                     help='Validate a set of CSV files given a set of rules.',
                                                     formatter_class=RawTextArgumentDefaultsHelpFormatter)
        validate_parser.add_argument('csv_files', nargs='+', help='The CSV files to include in the Excel file')
        validate_parser.add_argument('--rules_dir',
                                     type=dir_path,
                                     default=os.path.join(os.getcwd(), 'rules'),
                                     help='Directory path to rules')
        validate_parser.set_defaults(func=validate)

    def parse_args(self, args=None):
        self.args = self.parser.parse_args(args)

    def run(self):
        if not self.args:
            self.parse_args()
        # try:
        #     if not self.args:
        #         self.parse_args()
        # except:
        #     self.parser.print_help()
        #     sys.exit(1)
        _init_logger(getattr(logging, self.args.verbosity.upper()))
        logging.debug(f'command-line args: {self.args}')
        self.args.func(self.args)


class ColorLogFormatter(logging.Formatter):
    '''
    Custom formatter that changes the color of logs based on the log level.
    '''

    grey = "\x1b[38;20m"
    green = "\u001b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\u001b[34m"
    cyan = "\u001b[36m"
    reset = "\x1b[0m"

    timestamp = '%(asctime)s - '
    loglevel = '%(levelname)s'
    message = ' - %(message)s'

    FORMATS = {
        logging.DEBUG:    timestamp + blue + loglevel + reset + message,
        logging.INFO:     timestamp + green + loglevel + reset + message,
        logging.WARNING:  timestamp + yellow + loglevel + reset + message,
        logging.ERROR:    timestamp + red + loglevel + reset + message,
        logging.CRITICAL: timestamp + bold_red + loglevel + reset + message
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def _init_logger(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = ColorLogFormatter()
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class RawTextArgumentDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass


if __name__ == '__main__':
    App().run()
