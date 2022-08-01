#!/usr/bin/env python

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import pylint
from pylint.lint.utils import _temporary_sys_path

with _temporary_sys_path():
    pylint.modify_sys_path()
    pylint.run_pylint()
