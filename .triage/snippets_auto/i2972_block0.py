import pathlib
pathlib.Path('x') / '/foo'  # PosixPath('/foo')

import os
os.path.join('x', '/foo') # '/foo'
