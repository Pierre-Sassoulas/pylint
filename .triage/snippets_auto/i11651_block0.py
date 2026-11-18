# pylint: disable=missing-docstring
from zope.interface import Interface


class IThing(Interface):
    def __str__():
        """Return the string representation."""

    def method(arg):
        """Do something with arg."""


class ISubThing(IThing):
    def other(arg):
        """Do something else with arg."""
