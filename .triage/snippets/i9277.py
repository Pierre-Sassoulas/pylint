"""Repro attempt for the Windows 'charmap' codec report.

The crash was the text reporter writing a non-ASCII message to a
cp1252 stdout. On Linux, force the same stream encoding::

    PYTHONIOENCODING=cp1252 pylint i9277.py

That is an emulation, not a Windows run: only Windows can close it.
"""

# TODO: réparer le décodage — naïve
X = 1
