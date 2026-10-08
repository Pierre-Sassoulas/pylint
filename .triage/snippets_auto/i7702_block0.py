#!/usr/bin/python
"""Demonstrate pylint issue"""

import numpy

print([0,1,2,3][numpy.bitwise_xor.reduce([8,9])])
