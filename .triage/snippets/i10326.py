"""Repro for the sympy 'Building error' report.

The reporter's snippet imported minio; the sympy module named in their
traceback is the real trigger and blows the stack on its own.
"""

from sympy.polys.numberfields.resolvent_lookup import resolvent_coeff_lookup
