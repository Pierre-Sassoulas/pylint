import enum

class Transition(enum.IntEnum):
    ONE_ONE     = 1
    ONE_TWO     = 2
    ONE_THREE   = 3
    TWO_TWO     = 4
    TWO_THREE   = 5
    THREE_THREE = 6

class State(enum.IntEnum):
    ONE   = 1
    TWO   = 2
    THREE = 3

state1 = State.ONE
state2 = State.ONE
transition = None
if state1 == State.ONE:
    if state2 == State.ONE:
        transition = Transition.ONE_ONE
    elif state2 == State.TWO:
        transition = Transition.ONE_TWO
    elif state2 == State.THREE:
        transition = Transition.ONE_THREE
    else:
        pass
elif state1 == State.TWO:
    if state2 == State.ONE:
        transition = Transition.ONE_TWO  # [redefined-variable-type]
    elif state2 == State.TWO:
        transition = Transition.TWO_TWO
    elif state2 == State.THREE:
        transition = Transition.TWO_THREE
    else:
        pass
