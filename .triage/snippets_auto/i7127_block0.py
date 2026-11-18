class Grandparent:
    def __repr__(self):
        return "I'm a grandparent"


class Parent1(Grandparent):
    def __repr__(self):
        return "I'm parent 1"


class Parent2(Grandparent):
    def __repr__(self):
        return "I'm parent 2"


class Child1(Parent1, Parent2):  # [hidden-parent-method]
    pass


class Child2(Parent1, Parent2):
    def __repr__(self):
        return "no warning, because reimplemented completely"


class Child3(Parent1, Parent2):
    def __repr__(self):
        print("could emit a warning because not all parent methods delegate to super") # <-- AT ISSUE
        return super().__repr__()
