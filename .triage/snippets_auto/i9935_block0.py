def function1(value):  # argument is used
    return value


def function2(value):  # argument is unused, Pylint correctly reports it
    return 2


def function3(value):  # argument is unused, Pylint does not report
    raise ValueError
