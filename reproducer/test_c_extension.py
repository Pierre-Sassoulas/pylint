# This file is a reproducer for pylint issue #7585
# It demonstrates an infinite loop when c-extension-no-member is activated

import sys  # sys is a built-in C extension module

# This will trigger c-extension-no-member warning
# because sys is a C extension module
result = sys.non_existent_attribute  # This should trigger the warning
