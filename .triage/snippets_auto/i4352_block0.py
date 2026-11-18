#! /usr/bin/python3

# pylint: disable=missing-module-docstring

class Hello: # pylint: disable=too-few-public-methods
    """
    Some local class, but reproduced with external wtforms.FlaskForm, too.
    """

class World(Hello):
    """
    reported here:
    too-few-public-methods: Too few public methods (0/2)
    """
    def __init__(self):
        self.test = 0

