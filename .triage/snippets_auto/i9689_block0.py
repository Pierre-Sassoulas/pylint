# pylint: disable=missing-docstring, bare-except

def outer():
    a = 1
    def inner_try():
        try:
            nonlocal a
            print(a)  # E0601
            a = 2
            print(a)
        except:
            pass
    def inner_while():
        i = 0
        while i < 2:
            i += 1
            nonlocal a
            print(a)  # E0601
            a = 2
            print(a)
    def inner_for():
        for _ in range(2):
            nonlocal a
            print(a)  # correct
            a = 2
            print(a)
    inner_try()
    inner_while()
    inner_for()
outer()
