class Outer:
    def __init__(self):
        pass

    def say_hello(self):
        print("Hello World!")

    def make_inner(self):
        this = self

        class Inner:
            def get_outer(self):
                return this

        return Inner()


x = Outer().make_inner().get_outer()
x.say_hello()
