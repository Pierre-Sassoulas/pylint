# pylint: disable=missing-module-docstring, missing-function-docstring
# Using scipy.fft.rfft causes the error, removing this line also removes the error
# Seems related to issue #7702

import numpy as np
from scipy.fft import rfft


def some_func():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    arr_fft = rfft(arr)

    print(arr_fft[:, 0:2])
