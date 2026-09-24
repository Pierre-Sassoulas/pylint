class Base:
    def __init__(self):
        self.foo = "bar"

    @classmethod
    def from_dict(cls, values):
        return cls()


class Child(Base):
    def __init__(self):
        super().__init__()
        self.baz = "quz"

    @classmethod
    def from_dict(cls, values):
        return super().from_dict(values)


child = Child.from_dict({})
print(child.baz)
