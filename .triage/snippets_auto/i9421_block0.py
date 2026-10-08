# pylint: disable=missing-docstring


def target(*, right):
    del right


data = {"wrong": ...}

data.update({"right": ...})
# OR
# data["right"] = ...
# OR
# data.setdefault("right", ...)

data.pop("wrong")
# OR
# data.pop("wrong", None)
# OR
# del data["wrong"]

target(**data)
