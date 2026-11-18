def func(param1, /, param2: int):  # triggers `missing-type-doc` for "param2"
    """Does nothing.

    Parameters
    ----------
    param1
        A parameter.
    param2
        A parameter.
    """
    _ = param1, param2


class MyClass:
    def meth1(self, param1, /, param2: int):  # triggers `missing-type-doc` for "param1" and "param2"
        """Does nothing.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """
        _ = self, param1, param2

    def meth2(self, /, param1, param2: int):  # triggers `missing-type-doc` for "param2"
        """Does nothing.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """
        _ = self, param1, param2

    def meth3(self, param1, param2: int, /):  # triggers `missing-type-doc` for "param1" = OK
        """Does nothing.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """
        _ = self, param1, param2

    def meth4(self, /, param1: int, param2: int):  # triggers `missing-type-doc` for "param2"
        """Does nothing.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """
        _ = self, param1, param2
