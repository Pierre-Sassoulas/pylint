When calling a class method on a typevar defined using typing.Annotated, pylint erroneously reports no-member. 

The following code will reproduce the error:


from typing import Annotated

class Foo:
    @classmethod
    def foo(cls):
        print("foo called")

Bar = Annotated[Foo, int]

Bar.foo()
