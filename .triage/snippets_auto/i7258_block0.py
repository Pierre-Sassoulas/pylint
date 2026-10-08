from dataclasses import dataclass


class Chameleon:
    @dataclass
    class response:
        universe: int

    def __new__(cls, ultimate):
        return cls.response(ultimate * 3.5)


assert Chameleon(12).universe == 42
