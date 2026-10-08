pylint modifies source code that it reads from stdin.

See `...\pylint\lint\pylinter.py`


def _read_stdin() -> str:
    # See https://github.com/python/typeshed/pull/5623 for rationale behind assertion
    assert isinstance(sys.stdin, TextIOWrapper)
    sys.stdin = TextIOWrapper(sys.stdin.detach(), encoding="utf-8")
    return sys.stdin.read()
