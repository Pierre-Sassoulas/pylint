``unreachable-code`` now also fires for the body (and ``else``) of an ``if`` /
``while`` whose test never yields a value, and for the sibling after such a
statement (including ``assert``). Two trigger shapes are detected:

* the test is a direct call to a non-returning function (``sys.exit()``,
  ``exit()``, ``quit()``, ``os._exit()``, or a ``typing.NoReturn``-annotated
  function). ``visit_call`` already flagged the sibling for these; the body
  and ``else`` are now flagged too.
* the test always raises during ``bool()`` coercion. Currently this means
  ``NotImplemented`` on ``--py-version>=3.14``, where
  ``bool(NotImplemented)`` raises ``TypeError`` instead of returning ``True``.

Refs #11025
