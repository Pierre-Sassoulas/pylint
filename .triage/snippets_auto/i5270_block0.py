class Parent:
    def statement(self, *, future = None):
        pass

class Child(Parent):
    def statement(self, *, future):  # should emit 'signature-differs'
        pass
