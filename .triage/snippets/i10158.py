from typing import NotRequired, Required, TypedDict


class MyDict(TypedDict):
    required: Required[str]
    not_required: NotRequired[str]
    implicitely_required: str


def main():
    print(MyDict.__required_keys__)
    print(MyDict.__optional_keys__)


if __name__ == "__main__":
    main()
