from functools import singledispatch


class HasNoAttributeX:
    def __init__(self, not_attribute_x):
        self.not_attribute_x = not_attribute_x


class HasAttributeX:
    def __init__(self, attribute_x):
        self.attribute_x = attribute_x


@singledispatch
def example_singledispatch(argument):
    return argument


@example_singledispatch.register
def _(argument: HasNoAttributeX) -> HasAttributeX:
    return HasAttributeX(argument.not_attribute_x)


def example_function():
    argument = HasNoAttributeX(3)
    result = example_singledispatch(argument)
    assert result.attribute_x == 3
