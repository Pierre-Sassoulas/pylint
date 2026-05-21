Add the ``pylint-config upgrade`` command, which migrates a configuration file
across pylint breaking changes: it renames or removes obsolete options, and for
changes that have no single right answer it asks whether to keep the previous
behavior or adopt the new default. A new informational message,
``configuration-outdated``, points to the command when a configuration predates
the running pylint version.

Closes #5462
Closes #5465
