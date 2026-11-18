# pylint: disable=missing-docstring,raise-missing-from,no-self-use
def handle_exception():
    print("do anything there")
    raise Exception("oops")

try:
    1 // 0
except ZeroDivisionError:
    raise handle_exception()

class MyClass:
    def handle_exception(self):
        print("do anything there")
        raise Exception("oops")

    def my_method(self):
        try:
            1//0
        except ZeroDivisionError:
            raise self.handle_exception()
