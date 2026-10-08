def foo(arg):
    try:
        pass
    except: # doesn't trigger bare-except
        raise Exception()
