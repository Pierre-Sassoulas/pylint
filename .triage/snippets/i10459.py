"""Repro attempt for the scipy infinite-recursion report.

No longer recurses. It now draws ``no-name-in-module`` on a C
extension, which is a different bug.
"""

from scipy.special import erf
