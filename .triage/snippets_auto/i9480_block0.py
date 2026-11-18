This seems to be the same bug as #3904 but only affecting _nested_ yield expressions. The below example is adapted from the original issue.


# pylint: disable = disallowed-name
# pylint: disable = invalid-name
# pylint: disable = missing-function-docstring
# pylint: disable = missing-module-docstring

from typing import Callable, Generator

CHUNK_SIZE = 5


def chunk(handler: Callable[[str], None]) -> Generator[None, str, None]:
    buf = ""
    while True:
        while len(buf) < CHUNK_SIZE:
            buf += str((yield))  # Double parens required by Python syntax
        head, buf = buf[:CHUNK_SIZE], buf[CHUNK_SIZE:]

        handler(head)


def handle(contents: str) -> None:
    print(f"Got: {contents}")


streamer = chunk(handle)
next(streamer)  # start streaming
streamer.send("foo")
