import typing


class X(typing.Generic[typing.AnyStr]): ...


class Y(X[typing.AnyStr]): ...


class Z(typing.IO[typing.AnyStr]):
    """pretend full implementation here..."""


X[str]()
Y[str]()
Z[str]()
