from collections.abc import Callable


def type_changing_decorator(func: Callable[[int], int]) -> Callable[[int], str]:
    def wrapper(val: int) -> str:
        res = func(val)
        return f"the result is {res:d}"

    return wrapper


@type_changing_decorator
def add1(val: int) -> int:
    return val + 1


def main() -> None:
    res = add1(5)
    print(res.replace("the", "a"))


if __name__ == "__main__":
    main()
