Move documentation tests to tests directory
------------------------------------------

Move ``test_messages_documentation.py`` from the ``doc`` directory to ``tests/documentation/``.
Add a pytest marker to allow selectively running these tests with ``--run-documentation-tests``.
This addresses the issue of duplicate test runs while maintaining the ability to test documentation examples.
