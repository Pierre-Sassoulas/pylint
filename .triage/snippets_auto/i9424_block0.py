# pylint: disable=missing-docstring
class Base:
    @classmethod
    def apply(cls, *args, **kwargs):
        return cls.forward("ctx", *args, **kwargs)

    @staticmethod
    def forward(ctx, *args, **kwargs):
        raise NotImplementedError()


class Derived(Base):
    @staticmethod
    def forward(ctx, x, y):
        del x, y
        return ctx


Derived.apply(1, 2)
