"""Repro attempt for the 'Could not find <FunctionDef.warning_logger' report.

The reporter's stack came from haggis monkey-patching the logging
module at import time, so the ``add_trace_level()`` call is the part
that matters — a bare logging call never reproduced it.
"""

import logging

from haggis.logs import add_trace_level

add_trace_level()

_log: logging.Logger = logging.getLogger(__name__)


class Test:
    def somefunction(self):
        _log.warning("TEST")
