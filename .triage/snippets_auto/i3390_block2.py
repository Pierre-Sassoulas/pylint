def func(*, arg, arg2):
    # pylint: disable=unused-argument(arg2)
    return arg + 1

func(arg=1, arg2=2)
