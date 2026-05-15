from typing import ClassVar


class A:
    pass


class B:
    pass


A_B = tuple[A, B]


class C:
    a_b: ClassVar[A_B | None] = None

    @classmethod
    def cached_a_and_b(cls) -> A_B:
        if cls.a_b is None:
            cls.a_b = (A(), B())
        return cls.a_b

    @classmethod
    def f(cls) -> None:
        a, b = cls.cached_a_and_b()
        print(a, b)
