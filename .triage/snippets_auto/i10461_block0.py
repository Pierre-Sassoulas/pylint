def extends_class(cls):
    def decorator(f):
        setattr(cls, f.__name__, f)
    return decorator
