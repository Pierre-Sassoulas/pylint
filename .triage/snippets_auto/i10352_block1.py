"""A transform plugin that does nothing.

Strangely the issue only shows up when this plugin is active.
"""

from typing import Any

import astroid
import astroid.nodes
import astroid.manager


def func_annotations_filter(node: astroid.nodes.NodeNG) -> astroid.nodes.NodeNG:
    """Filter FunctionDefs"""

    # Do nothing.
    return node


def register(linter: Any) -> None:  # pylint: disable=unused-argument
    """Unused here; we're only registering plugins."""


def register_plugins(manager: astroid.manager.AstroidManager) -> None:
    """Register a transform for FunctionDef that does nothing."""
    manager.register_transform(astroid.FunctionDef, func_annotations_filter)


register_plugins(astroid.MANAGER)
