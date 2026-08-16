"""A name redefining an import is still checked against ``bad-names``.

The name is spelled by the import, so its style is not checked, but the
blocklist still applies. This already held at module scope; it now holds
inside a function too.
"""
try:
    from os.path import isfile as foo
except ImportError:
    foo = None  # [disallowed-name]


def eat():
    """The same shape, one scope down."""
    try:
        from os.path import isdir as bar  # pylint: disable=import-outside-toplevel
    except ImportError:
        bar = None  # [disallowed-name]
    return bar


print(foo, eat())
