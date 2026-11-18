"""
Sample test module
"""

import sys
import unittest.mock


@unittest.mock.patch.object(sys, 'version')
def get_version(version):
    """
    Decorated function
    """
    print(version)

def test_1():
    """
    Calling a decorated function
    """
    get_version()
