def convert_type(
    x, type
):  # pylint: disable=missing-function-docstring,redefined-builtin
    return type(x)


convert_type(12.34, str).split(".")
