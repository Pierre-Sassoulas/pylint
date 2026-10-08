# pylint: disable=missing-module-docstring,unused-argument
# pylint: disable=missing-function-docstring,unused-variable
# pylint: disable=too-many-arguments

# ruler:
# .......1.........2.........3.........4.........5.........6.........7....79->|

def first_case() -> None:
    # next line generates 'line-too-long' error (as it should)
    def my_function(aaa: int, bbb: int, ccc: int, ddd: int) -> int:  # pragma: no cover
        return 0

def second_case() -> None:
    # next line generates 'useless-suppression' (which is wrong)
    def my_function(aaa: int, bbb: int, ccc: int, ddd: int) -> int:  # pragma: no cover  # pylint: disable=line-too-long
        return 0

def third_case() -> None:
    # this case works as expected
    # pylint: disable-next=line-too-long
    def my_function(aaa: int, bbb: int, ccc: int, ddd: int) -> int:  # pragma: no cover
        return 0

def fourth_case() -> None:
    # this case works as expected
    def my_function(aaa: int, bbb: int, ccc: int, ddd: int, eee: int, fff: int, ggg: int) -> int:  # pragma: no cover  # pylint: disable=line-too-long
        return 0

# ruler again:
# .......1.........2.........3.........4.........5.........6.........7....79->|
