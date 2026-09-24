from dataclasses import dataclass


@dataclass
class One:
    f_one: str
    f_two: str


@dataclass
class Two:
    f_three: str
    f_four: One

    def __post_init__(self):
        self.f_four = One(**self.f_four)


data = {"f_three": "three", "f_four": {"f_one": "one", "f_two": "two"}}
print(Two(**data))
