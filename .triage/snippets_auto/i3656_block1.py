def foo(arg):
    try:
        pass
    except: # doesn't trigger bare-except
        if arg:
            return
        raise Exception()
