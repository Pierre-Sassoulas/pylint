$ cat pylint_bug/__init__.py
''' Simple reproducer for Pylint 'import-self' false positive. '''
from . import misspelled_module_name
