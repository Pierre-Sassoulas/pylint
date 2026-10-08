class ParentMetaclass(type):
    def __init__(cls, what, bases=None, attrs=None):
        super().__init__(what, bases, attrs)

        cls.aloha = 'test'


class Parent(metaclass=ParentMetaclass):
    def handle(self):
        raise NotImplementedError


class Test(Parent):
    def handle(self) -> None:
        return self.aloha  # false positive [no-member]
