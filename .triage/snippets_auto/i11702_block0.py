"""Test."""

import logging


def old_style_lazy(one, two):
    """Test."""
    # Warns about `logging-too-many-args` when using `--logging-format-style new`
    logging.info("test %s", one)
    logging.info("test %s %s", one, two)


def new_style_lazy(one, two):  # Does not work with std-lib!
    """Test."""
    # Warns about `logging-too-many-args` when using `--logging-format-style old`
    logging.info("test {}", one)
    logging.info("test {} {}", one, two)
