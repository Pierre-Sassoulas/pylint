"""Data model methods that bad-dunder-name does not know."""


class Meta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return {}


class Base:
    def __mro_entries__(self, bases):
        return (object,)


class Buffer:
    def __buffer__(self, flags):
        return memoryview(b"x")

    def __release_buffer__(self, view):
        view.release()


class Point:
    def __replace__(self, **changes):
        return self
