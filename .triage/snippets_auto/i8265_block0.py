class Cls:
    def __init__(self, foobar):
        self.foobar = foobar

    def get_foobar(self):
        return self.foobar

def test(class_ref, method_ref):
    print(method_ref)
    # <function Cls.get_foobar at 0x7f0e0f151f80>

    instance = class_ref(1234)
    bound_method = method_ref.__get__(instance, class_ref)
    # ^- C2801: Unnecessarily calls dunder method __get__. Use get method. (unnecessary-dunder-call)

    print(bound_method)
    # <bound method Cls.get_foobar of <__main__.Cls object at 0x7fc81afa6d90>>
    print(bound_method())
    # 1234

test(Cls, Cls.get_foobar)
