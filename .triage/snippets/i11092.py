"""Repro attempt for the PyPy getset_descriptor report.

Reported on Windows PyPy 3.11 with astroid 4.0.4 / 4.2.0b3. Clean under
Linux PyPy 3.11.15 with astroid 4.3.1.
"""

import sys

if __name__ == '__main__':
    print(f"#V1 {sys.version=:}")
