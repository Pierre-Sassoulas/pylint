A = 1
class Foo:
    global A
    A = 2

print(Foo.A)
