# pylint: enable=undefined-variable
def func():
    x: int
    return [
        x  # <-- error
        for i in range(2)
        if (x := i)
    ]
