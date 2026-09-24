class E:
    @classmethod
    @property
    def p(cls):
        return 0, 42


x, y = E.p
