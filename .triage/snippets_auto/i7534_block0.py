class ContextManaged:

    def __exit__(exc_type, exc_value, traceback):
        ...  # SEE: https://docs.python.org/3/reference/datamodel.html#object.__exit__

    def __exit__(self, exception_type, exception_value, exception_traceback):
        ...  # SEE: https://www.geeksforgeeks.org/__exit__-in-python/

    def __exit__(self, t, value, traceback):
        ...  # SEE: https://github.com/python/mypy/issues/4885

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...  # PyCharm autocomplete

    def __exit__(self, t, value, tb):
        ...
