"""Repro attempt for the ``'UninferableBase' object is not iterable`` report.

This is the reporter's own reduction, not their full file.
"""

import pytz
from bson.json_util import LEGACY_JSON_OPTIONS

CUSTOM_JSON_OPTIONS = LEGACY_JSON_OPTIONS.with_options(tz_aware=True, tzinfo=pytz.UTC)
