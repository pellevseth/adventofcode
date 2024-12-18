# coding: utf-8
import importlib

__author__ = 'tve'

import sys
import textwrap

try:
    import pwd
except:
    pass

import os
import argparse
from datetime import datetime
from argparse import RawTextHelpFormatter

from core import baselogger

logger = baselogger.getLogger(__name__)

program_description = 'Gnucash stuff'


def find_commands(path):
    """
    :param path: the path to search for functions that can be run
    :return:
    """
    return [f[:-3] for f in os.listdir(path) if not f.startswith('_') and f.endswith('.py')]


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def run_from_cmd_line(argv):
    """Run the command from command line. Setup logging and parser for the functions.
    :param argv: Arguments from command line
    :return:
    """
    common_parser = argparse.ArgumentParser(argv, formatter_class=RawTextHelpFormatter, add_help=False)
    common_parser.add_argument('--verbose', action='store_true', default=False,
                               help='Verbose logging. Logs everything and overrides --log_level')
    common_parser.add_argument('--log_level', default='INFO', choices=['ERROR', 'WARNING', 'QA', 'INFO', 'DEBUG'],
                               help='Log on this level. --Verbose sets it to lowest level')
    root_parser = MyParser(argv, formatter_class=RawTextHelpFormatter, parents=[common_parser])
    root_parser.description = program_description

    # Add subparser arguments
    add_command_parsers(root_parser, common_parser)

    # Parse the command line arguments
    args = root_parser.parse_args(argv)

    # Start up the logger
    if args.verbose:
        baselogger.init_logger(0)
    else:
        baselogger.init_logger(args.log_level)
    logger.qa('-' * 30 + '\n')
    try:
        user = pwd.getpwuid(os.getuid())[0]
    except:
        user = ''
    logger.qa('%s:\nUser: %s\nCommand: %s\nArguments: %s\n',
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              user,
              argv[0],
              argv[1:])

    # Execute command
    args.func(**vars(args))


def add_command_parsers(parser, logparser):
    """Add subparser for each available command.
    :param parser: Root parser
    :return:
    """
    subparsers = parser.add_subparsers(metavar='Command')
    help_text = 'ONE OF THE FOLLOWING:\n'
    available_commands = find_commands(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'functions'))
    max_length = max([len(a) for a in available_commands])
    for command in available_commands:
        child_parser = subparsers.add_parser(command, parents=[logparser])
        call = importlib.import_module('functions.%s'%  command)
        if hasattr(call, 'set_argparser'):
            call.set_argparser(child_parser)
        else:
            child_parser.description = 'Description is missing'
        help_text += command + ": " + " "*(max_length-len(command)) + ('\n'+' '*(max_length+2)
                                                                       ).join(textwrap.wrap(child_parser.description,60)) + '\n'
        child_parser.set_defaults(func=call.main)
    subparsers.help = help_text + '\nType "Command --help" for more information about given command'