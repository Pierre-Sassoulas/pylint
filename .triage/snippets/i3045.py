class MyClass:
    _all = None

    @classmethod
    def all(cls):
        if not cls._all:
            cls._all = find_all()
        return cls._all

    @classmethod
    def exist(cls, number):
        return number in cls.all()


def find_all():
    return [1, 2, 3]


if __name__ == "__main__":
    assert MyClass.exist(2)
