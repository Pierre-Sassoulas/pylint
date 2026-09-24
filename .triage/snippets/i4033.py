class Bang(Exception):
    def __init__(self, required):
        super().__init__(f"{required}")


def false_negative():
    raise Bang


def work_correctly():
    raise Bang()
