import attr

class Base:
    def __init__(self):
        pass

@attr.s(auto_attribs=True)
class Sub(Base):
    value: int

print(Sub(123))
