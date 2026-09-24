"""Repro attempt for the ``'Deprecated' object has no attribute '__dict__'`` report.

Run it twice: plain, and with ``--unsafe-load-any-extension=y``, which
is the option the report named.
"""

from black import FileMode
