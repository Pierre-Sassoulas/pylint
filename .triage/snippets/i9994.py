class Base:
    def __init__(self, *args, **kwargs):
        pass


class Derived(Base):
    def __init__(self):
        super().__init__()


class MyException(Exception):
    def __init__(self):
        super().__init__()
