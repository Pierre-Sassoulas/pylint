def preprocess(bar: str) -> str:
    return bar + "xyz"


def condition1(foo):
    return foo.startswith("abc")


def condition2(foo):
    return "bcdef" in foo


def postprocess(foo):
    return foo


data = ["abcdef", "qwerty"]


def decorator(arg):
    print(f"{arg=}")
    return lambda x: x


@decorator(
    [
        postprocess(foo)
        for string in data
        if condition1(foo := preprocess(string)) and condition2(foo)
    ],
)
def decorated() -> None:
    pass
