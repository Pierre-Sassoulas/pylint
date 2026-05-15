from enum import Enum

Direction = Enum("Direction", ["LEFT", "RIGHT", "BOTH"])


def check_direction(direction):
    if not isinstance(direction, Direction):
        raise TypeError(f'Not a Direction ("{direction}" is a {type(direction)})')
