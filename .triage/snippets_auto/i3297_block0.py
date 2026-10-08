#!/usr/bin/env python
"""lorem ipsum"""

import numpy as np


def get(greater):
    """lorem ipsum"""
    ret = np.arange(10)
    if greater:
        f = ret > 5
        ret = ret[f].copy()  # The bug is here ...
    else:
        f = ret <= 5  # f is not used - to be detected => pylint feature request (W0602?)
    # ... the line of the bug shoud be here instead
    return ret


if __name__ == "__main__":
    print(get(True))
    print(get(False))
