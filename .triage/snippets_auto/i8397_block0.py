import threading
import multiprocessing

def add(a: int, b: int) -> None:
    print(a + b)

threading.Thread(
    target = add,
    args = (4, 5),
).run()  # prints 9

multiprocessing.Process(
    target = add,
    args = (6, 7),
).run()  # prints 13

threading.Thread(
    target = add,
    args = (4,),
).run()  # error at runtime, but no warning

multiprocessing.Process(
    target = add,
    args = (6,),
).run()  # error at runtime, but no warning
