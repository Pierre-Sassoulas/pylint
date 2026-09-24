class Unknown:
    CONSTANT_1 = 0
    CONSTANT_2 = 1
    CONSTANT_3 = 2

    @classmethod
    @property
    def all_constants(cls) -> list[int]:
        return [cls.CONSTANT_1, cls.CONSTANT_2, cls.CONSTANT_3]


print(Unknown.all_constants[0])
