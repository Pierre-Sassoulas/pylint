from dataclasses import dataclass

@dataclass
class Counter:
    count: int = 0

    def increment(self) -> Counter:  # consider-using-self
        self.count += 1
        return self

    def copy(self) -> Counter:  # not Self
        return Counter(self.count)
