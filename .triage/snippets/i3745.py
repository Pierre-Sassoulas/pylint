class Base:
    def __init__(self, func):
        self.func = func


class Extended(Base):
    def __init__(self):
        pass

    def func(self, arg):
        print(arg)
