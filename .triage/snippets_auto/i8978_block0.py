"https://github.com/pylint-dev/pylint/issues/8978"

class Incrementable:
    "class with an incrementable field"
    def __init__(self, a):
        self.a = a
    def __iadd__(self, other):
        if isinstance(other, Incrementable):
            self.a += other.a
            return self
        return NotImplemented

d = {}
d.setdefault("a", Incrementable(6)).__iadd__(Incrementable(7))
