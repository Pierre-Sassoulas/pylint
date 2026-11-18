# pylint: disable=missing-module-docstring
# pylint: disable=multiple-imports

import shutil, sys

if sys.version_info >= (3, 13):
    shutil.chown('/tmp/doesntexist', 222, 222, follow_symlinks=False)
else:
    shutil.chown('/tmp/doesntexist', 222, 222)
