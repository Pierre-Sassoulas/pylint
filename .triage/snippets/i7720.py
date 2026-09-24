class Converter:
    def register(self):
        def decorator(cls):
            return cls

        return decorator


class MyContainer:
    CONVERTER = Converter()

    @CONVERTER.register()
    class NamedArray:
        def __init__(self, *args, **kwargs):
            pass
