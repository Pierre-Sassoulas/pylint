"""Unused disables for two exempt messages."""


def first():
    """Uses nothing deprecated."""
    return 1  # pylint: disable=deprecated-method


def second():
    """No import cycle here."""
    return 2  # pylint: disable=cyclic-import
