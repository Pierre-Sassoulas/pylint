def function_a() -> None:
    print("a")


def function_b() -> None:
    print("b")


def test1(function_to_choose: str) -> None:
    match function_to_choose:
        case "a":
            function = function_a
        case "b":
            function = function_b
        case "c":

            def function() -> None:
                print("case c")

        case _:
            raise AssertionError(function_to_choose)

    function()
