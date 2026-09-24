def foobar(x):
    if x not in ["A"]:
        v = []

    if x == "B":
        print(v)
    elif x == "A":
        v = []
    else:
        raise RuntimeError(f"{x}")
