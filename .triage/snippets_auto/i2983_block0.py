"""Minimal repro for pylint's not-an-iterable error.
"""
from typing import List

import attr


class Model(object):
    """Basic model showing pylint's not-an-iterable error.
    """

    @classmethod
    def attributes(cls):
        # type: () -> List[str]
        """Get attributes of a model.
        """
        # The iteration here triggers the warning
        return [a.name for a in attr.fields(cls)]


@attr.s
class Basic(Model):
    """Basic model that's inherited, showing pylint's not-an-iterable error.
    """
    hello = attr.ib()  # type: str

assert Basic.attributes() == "hello"
