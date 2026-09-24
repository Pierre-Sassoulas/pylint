import numpy as np
from scipy import stats as st

print(st.entropy([1, 2, 3, np.nan], nan_policy="omit"))
