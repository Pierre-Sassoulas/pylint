The code below runs fine, but pylint reports the error "No name '_' in module 'ibis' [no-name-in-module] against the line starting "from ibis...". 

-------------------

"""Test code"""

import ibis
from ibis import _
import pandas as pd

ibis.options.interactive = True

df = ibis.memtable(
    pd.DataFrame(
        [["a", 1, 2], ["b", 3, 4]],
        columns=["one", "two", "three"],
        index=[5, 6],
    )
)

df.select(_.one, _.two)
