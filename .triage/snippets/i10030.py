from dataclasses import dataclass


@dataclass
class A:
    f: "list[int] | None"
