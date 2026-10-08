"""Module docstring."""

class Foo:
    """Foo class."""

    @classmethod
    def bar_clsmethod(cls):
        """Bar method."""
        return cls()

    def a_public_method(self):
        """A public method."""
        print('Hello world.  I am:', self)


class Bar(Foo):
    """Bar class."""

    @classmethod
    def bar_clsmethod(cls):
        instance = super(Bar, cls).bar_clsmethod()
        instance.a_public_method()
        instance.method()  # no-member
        return instance

    def method(self):
        """Say hello to the world."""
        print('Hello World', self)
