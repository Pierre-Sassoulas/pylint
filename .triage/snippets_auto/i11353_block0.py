# Simple package layout:

#   pkg/
#       __init__.py
#       utils/
#           __init__.py
#           foo.py
#           json.py

# Content of json.py:

ONE = 1

# Content of foo.py:

import json
import re
import re as re1                  # triggers `reimported` -> OK

from . import json as my_json     # triggers `reimported` -> false positive

from .json import ONE             # does not trigger -> OK
