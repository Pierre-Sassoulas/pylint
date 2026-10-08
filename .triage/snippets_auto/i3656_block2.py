def foo(arg):
    try:
        pass
    except: # does trigger bare-except
        if not arg:
            raise Exception()
        return
