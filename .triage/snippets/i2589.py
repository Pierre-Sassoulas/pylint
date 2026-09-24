def foo():
    import os.path  # pylint: disable=import-outside-toplevel

    print(os.path.exists("/tmp"))
