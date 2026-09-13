Add the new ``init_order`` optional extension, providing
``access-member-before-initialization`` (``E3901``). It is raised when the
constructor calls a method that reads an instance attribute the constructor
only assigns later: the attribute does not exist yet when the method runs, so
building the object raises an ``AttributeError``.

Closes #11338
