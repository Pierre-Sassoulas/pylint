def f1(i: int) -> None:
    print(i)


def f2() -> None:
    r = f1(2)  # assignment-from-no-return
    if not r:
        print("error")
    if not f1(2):  # no error
        print("error")
