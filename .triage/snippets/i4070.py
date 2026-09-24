from typing import NamedTuple


class Lines(NamedTuple):
    lines: list[str]

    def add_line(self, line: str) -> "Lines":
        return self._replace(lines=self.lines + [line])


if __name__ == "__main__":
    lines = Lines(lines=[])
    print(repr(lines.add_line("Live long and prosper!")))
