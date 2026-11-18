from typing import Callable, Concatenate, ParamSpec, TypeVar

S = TypeVar('S')
P = ParamSpec('P')
RealFun = Callable[Concatenate[S, P], None]
FunWithEvent = Callable[Concatenate[S, int, P], None]


def run_event() -> Callable[[RealFun[S, P]], FunWithEvent[S, P]]:
    def wrapper(func: RealFun[S, P]) -> FunWithEvent[S, P]:
        def wrapped(self: S, event: int, *args: P.args, **kwargs: P.kwargs) -> None:
            func(self, *args, **kwargs)
        return wrapped
    return wrapper


class SomeClass:
    @run_event()
    def orig_fun(self) -> None:
        pass

    def do_call1(self) -> None:
        self.orig_fun(42) # That's OK

    def do_call2(self) -> None:
        self.orig_fun()  # This is an error, MyPy finds that, Nice

    def do_call3(self) -> None:
        self.orig_fun('q')  # This is an error, MyPy finds that, Nice

    def do_call4(self) -> None:
        self.orig_fun(42, 'q')  # This is an error, MyPy finds that, Nice
