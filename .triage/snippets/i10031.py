class Ints(set[int]):
    def __init__(self):
        self |= {0}
        self.member = True

    def method(self) -> None:
        print(self.member)


print(list(Ints()))
print(Ints().member)
