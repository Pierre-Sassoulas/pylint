import sys


def stdin_peek():
    return sys.stdin.buffer.peek(16)
