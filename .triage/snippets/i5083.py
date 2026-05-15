class Parent:
    def __init__(self, linker, handler):
        pass


class Child(Parent):
    def __init__(self, linker, handler):
        Parent.__init__(self, linker, handler)
