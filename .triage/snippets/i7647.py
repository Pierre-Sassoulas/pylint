from contextlib import ExitStack


def fun(**kwargs):
    print(kwargs)


def run_in_context(callable_):
    with ExitStack():
        callable_()


def main(omit_arg: bool):
    kwargs = {} if omit_arg else {"arg": 2}
    run_in_context(lambda: fun(**kwargs))
