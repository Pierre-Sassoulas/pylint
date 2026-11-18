def __getattr__(name, /):
    if name == 'foo':
        global foo
        from .mod import foo
        return foo
    if name == 'bar':
        global bar
        import warnings
        warnings.warn('"bar" is deprecated; use "baz" instead', DeprecationWarning, stacklevel=2)
        bar = baz
        return bar
    if name == 'spam':
        global spam
        import ham
        def spam():
            for _ in range(5):
                ham.eggs()
       return spam
