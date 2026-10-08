"https://github.com/pylint-dev/pylint/issues/10440"
import numpy as np
mx = np.random.normal(size=(5,5))
i, j = np.unravel_index(np.argmax(mx), mx.shape)
