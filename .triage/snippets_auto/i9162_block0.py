def util_func(stack):
    tmpdir = stack.enter_context(tempfile.TemporaryDirectory())
    # do stuff
    return tmpdir

def test_something():
    with contextlib.ExitStack() as stack:
        tmpdir = util_func(stack)
        stack.enter_context(tempfile.NamedTemporaryFile(dir=tmpdir))
        # ...
