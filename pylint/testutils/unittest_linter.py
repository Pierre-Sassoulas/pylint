# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=duplicate-code

from __future__ import annotations

from typing import Any, Literal

from astroid import nodes

from pylint.interfaces import UNDEFINED, Confidence, _confidence_or_undefined
from pylint.lint import PyLinter
from pylint.testutils.output_line import MessageTest


class UnittestLinter(PyLinter):
    """A fake linter class to capture checker messages."""

    def __init__(self) -> None:
        self._messages: list[MessageTest] = []
        super().__init__()

    def release_messages(self) -> list[MessageTest]:
        try:
            return self._messages
        finally:
            self._messages = []

    def add_message(
        self,
        msgid: str,
        line: int | None = None,
        # TODO: Make node non optional
        node: nodes.NodeNG | None = None,
        args: Any = None,
        confidence: Confidence | None = UNDEFINED,
        col_offset: int | None = None,
        end_lineno: int | None = None,
        end_col_offset: int | None = None,
    ) -> None:
        """Add a MessageTest to the _messages attribute of the linter class."""
        confidence = _confidence_or_undefined(confidence, stacklevel=2)
        # Look up "location" data of node if not yet supplied
        if node:
            node_line, node_col, node_end_line, node_end_col = self._node_position(node)
            if line is None:
                line = node_line
            if col_offset is None:
                col_offset = node_col
            if end_lineno is None:
                end_lineno = node_end_line
            if end_col_offset is None:
                end_col_offset = node_end_col

        self._messages.append(
            MessageTest(
                msgid,
                line,
                node,
                args,
                confidence,
                col_offset,
                end_lineno,
                end_col_offset,
            )
        )

    def add_message_at_node(
        self,
        msgid: str,
        node: nodes.NodeNG,
        args: Any = None,
        confidence: Confidence = UNDEFINED,
    ) -> None:
        """Add a MessageTest to the _messages attribute of the linter class.

        Records the same ``MessageTest`` as ``add_message(msgid, node=node)``, so
        checker tests keep passing when a checker switches to this method.
        """
        line, col_offset, end_lineno, end_col_offset = self._node_position(node)
        self._messages.append(
            MessageTest(
                msgid,
                line,
                node,
                args,
                confidence,
                col_offset,
                end_lineno,
                end_col_offset,
            )
        )

    def add_message_at_location(
        self,
        msgid: str,
        *,
        module: str,
        filepath: str | None = None,
        lineno: int | None = None,
        col_offset: int | None = None,
        end_lineno: int | None = None,
        end_col_offset: int | None = None,
        args: Any = None,
        confidence: Confidence = UNDEFINED,
    ) -> None:
        """Add a MessageTest to the _messages attribute of the linter class."""
        self._messages.append(
            MessageTest(
                msgid,
                lineno,
                None,
                args,
                confidence,
                col_offset,
                end_lineno,
                end_col_offset,
            )
        )

    @staticmethod
    def is_message_enabled(*unused_args: Any, **unused_kwargs: Any) -> Literal[True]:
        return True
