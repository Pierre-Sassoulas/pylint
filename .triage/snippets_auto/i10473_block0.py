a = 1
def f(b):
    if not b:
        global a # Irrespective of the value of `b`, `a` is declared a `global` and it can be modified globally in the `else` branch
    else:
        a = 2
    print(a)
