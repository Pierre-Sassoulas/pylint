class Base(Exception):
    def __init__(self):
        super().__init__()
        self.common_field = ""


class Child(Base):
    def __init__(self):
        super().__init__()
        self.child_field = ""


def foo() -> str:
    try:
        pass
    except Base as ex:
        match ex:
            case Child():
                # noinspection PyUnresolvedReferences
                return ex.child_field
            case _:
                return ex.common_field


def bar(ex: Base) -> str:
    match ex:
        case Child():
            # noinspection PyUnresolvedReferences
            return ex.child_field
        case _:
            return ex.common_field
