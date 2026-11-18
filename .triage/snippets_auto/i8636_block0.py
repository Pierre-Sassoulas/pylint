from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

def foo(color: Color):
    match color:
        case Color.RED:
            print(255,0,0)
        case color.GREEN:
            print(0,255,0)
