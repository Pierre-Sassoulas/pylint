# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import enum


class Intention(enum.Enum):
    KEEP = "Keep the same behavior"
    USE_DEFAULT = "Use the new default behavior"
    # This could/should always be automated
    FIX_CONF = "Fix the configuration to become consistent again"
