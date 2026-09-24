"""Repro attempt for the xarray recursion report.

The reporter's MRE only recursed when the subclass lived inside a
package: copy this into ``mylib/__init__.py`` and lint ``mylib`` — as a
standalone file it never reproduced even when the bug was live.
"""

import xarray as xr


class A(xr.DataArray):
    ...
