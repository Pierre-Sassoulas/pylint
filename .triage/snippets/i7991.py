class Foo:
    def save(self):
        return self


class Bar(Foo):
    def __init__(self) -> None:
        self.value = 12

    def save(self):
        return super().save()


print(Bar().save().value)
