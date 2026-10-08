''' Reproducer for false positive on PyPy-based Pylint. '''

import sys
from ctypes import Structure, c_ssize_t, c_void_p
from sys import implementation

class Class( type ): ''' Trivial metaclass. '''
class Object: ''' Trivial class. '''

if 'cpython' == implementation.name and not hasattr( sys, 'getobjects' ):
    class PyObject( Structure ):
        ''' Structural representation of normal :c:struct:`PyObject`. '''
        _fields_ = (
            ( 'ob_refcnt', c_ssize_t ),
            ( 'ob_type', c_void_p )
        )
    new_metaclass_pointer = id( Class )
    class_struct = PyObject.from_address( id( Object ) )
    class_struct.ob_type = c_void_p( new_metaclass_pointer )
    new_metaclass_struct = PyObject.from_address( new_metaclass_pointer )
    new_metaclass_struct.ob_refcnt += 1  # On PyPy, complains about 'no-member'

    print( type( Object ) )
