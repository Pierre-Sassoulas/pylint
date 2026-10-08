#!/usr/bin/env python

"""
Demonstrates that Pylint raises no-member when accessing existing members
of an argparse result.

Required ingredients:
- This happens only on Python 3.9, but not on earlier Python versions.
- This happens only when argparse.ArgumentParser is subclassed.
- This happens only for the '--logdir' option, but not for the 'name'
  positional argument. However, in our real case with more options, it also
  happened for positional arguments.
"""

import argparse


class SilentArgumentParser(argparse.ArgumentParser):
    """
    argparse.ArgumentParser subclass that silences any errors and exit and
    just raises them as SystemExit.
    """

    def error(self, message=None):
        """Called for usage errors detected by the parser"""
        raise SystemExit(2)

    def exit(self, status=0, message=None):
        """Not sure when this is called"""
        raise SystemExit(status)


def parse_args(argv):
    """
    Parse the command line arguments.
    """
    parser = SilentArgumentParser()

    parser.add_argument('--logdir', type=str, default=None)
    parser.add_argument('name', type=str, default=None)

    parsed_args = parser.parse_args(argv)
    return parsed_args


args = parse_args(['foo'])
print(repr(args))
print(args.name)
print(args.logdir)  # Pylint issues no-member on Python 3.9
