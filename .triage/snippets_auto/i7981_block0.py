# pylint disable=missing-docstring

import numpy as np

arr = np.arange(10)
arr = np.pad(arr, (2, 4))
print(arr.strides[0])
