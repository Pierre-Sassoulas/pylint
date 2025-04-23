# This file is a reproducer for pylint issue #7585
# It demonstrates an infinite loop when c-extension-no-member is activated

import numpy as np

# This will trigger c-extension-no-member warning
# because numpy is a C extension module
array = np.array([1, 2, 3])
result = array.non_existent_method()  # This should trigger the warning
