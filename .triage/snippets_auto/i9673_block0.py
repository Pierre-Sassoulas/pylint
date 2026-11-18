# pylint: disable=missing-module-docstring,missing-class-docstring,too-few-public-methods

def func1():
    # pylint: disable=line-too-long
    print('looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong statement')
    # pylint doesn't like this long comment if it's after all this function's statements, but it's fine if there are no more statements in the module after this function
    # pylint: enable=line-too-long

print()
