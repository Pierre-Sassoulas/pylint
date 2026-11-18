from . import mod2

class SubClass(mod2.SuperClass):
    def __init__(self):
        super().__init__()
        self.attr2 = None

    def meth1(self):
        if not self.attr1:
            return
        self.attr1 = "Something"
