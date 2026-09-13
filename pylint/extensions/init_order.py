# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check that ``__init__`` assigns an attribute before calling a method reading it."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import astroid
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter

# Statements that always run once reached. The analysis stops at the first
# statement that is not one of those: what a condition, a loop or a try
# assigns is not guaranteed to have happened.
SIMPLE_STATEMENTS = (
    nodes.AnnAssign,
    nodes.Assert,
    nodes.Assign,
    nodes.AugAssign,
    nodes.Delete,
    nodes.Expr,
    nodes.Global,
    nodes.Import,
    nodes.ImportFrom,
    nodes.Nonlocal,
    nodes.Pass,
    nodes.Raise,
    nodes.Return,
)

# Defining one of those means attributes can appear without an assignment.
DYNAMIC_ATTRIBUTE_METHODS = frozenset(
    {"__getattr__", "__getattribute__", "__setattr__"}
)


def _simple_statements(body: list[nodes.NodeNG]) -> Iterator[nodes.NodeNG]:
    """Yield the leading statements of *body* that are known to always run."""
    for statement in body:
        if not isinstance(statement, SIMPLE_STATEMENTS):
            return
        yield statement


def _self_name(method: nodes.FunctionDef) -> str | None:
    """Return the name the method uses for the instance, usually ``self``."""
    if method.type != "method" or method.decorators:
        return None
    arguments = method.args.args
    return arguments[0].name if arguments else None


def _is_self_attribute(node: nodes.NodeNG, self_name: str) -> bool:
    return (
        isinstance(node, (nodes.Attribute, nodes.AssignAttr, nodes.DelAttr))
        and isinstance(node.expr, nodes.Name)
        and node.expr.name == self_name
    )


def _assigned_attributes(statement: nodes.NodeNG, self_name: str) -> set[str]:
    return {
        assignment.attrname
        for assignment in statement.nodes_of_class(nodes.AssignAttr)
        if _is_self_attribute(assignment, self_name)
    }


def _deleted_attributes(statement: nodes.NodeNG, self_name: str) -> set[str]:
    return {
        deletion.attrname
        for deletion in statement.nodes_of_class(nodes.DelAttr)
        if _is_self_attribute(deletion, self_name)
    }


def _escapes(call: nodes.Call, self_name: str) -> bool:
    """Whether *call* could initialize the instance out of sight.

    That is the case when the instance is handed over as an argument, when a
    parent constructor runs, and when a method call cannot be resolved.
    """
    keywords = call.keywords or ()
    for argument in (*call.args, *(keyword.value for keyword in keywords)):
        if isinstance(argument, nodes.Starred):
            argument = argument.value
        if isinstance(argument, nodes.Name) and argument.name == self_name:
            return True
    return any(
        isinstance(name, nodes.Name) and name.name == "super"
        for name in call.func.nodes_of_class(nodes.Name)
    )


def _assigned_anywhere(method: nodes.FunctionDef) -> set[str]:
    """Return every attribute *method* can assign, wherever it does it."""
    self_name = _self_name(method)
    if self_name is None:
        return set()
    return _assigned_attributes(method, self_name)


def _read_attributes(method: nodes.FunctionDef, self_name: str) -> Iterator[str]:
    """Yield the attributes *method* reads before assigning them itself."""
    assigned: set[str] = set()
    for statement in _simple_statements(method.body):
        for attribute in statement.nodes_of_class(nodes.Attribute):
            if _is_self_attribute(attribute, self_name):
                if attribute.attrname not in assigned:
                    yield attribute.attrname
        # ``self.apple += 1`` reads ``self.apple`` too, but astroid only records
        # the target as an assignment.
        if isinstance(statement, nodes.AugAssign) and _is_self_attribute(
            statement.target, self_name
        ):
            if statement.target.attrname not in assigned:
                yield statement.target.attrname
        assigned |= _assigned_attributes(statement, self_name)
        assigned -= _deleted_attributes(statement, self_name)


def _find_early_accesses(
    klass: nodes.ClassDef, init: nodes.FunctionDef, self_name: str
) -> Iterator[tuple[nodes.Call, str, str, int]]:
    """Yield the calls of *init* reading a member it has not assigned yet."""
    assigned: set[str] = set()
    for statement in _simple_statements(init.body):
        for call in statement.nodes_of_class(nodes.Call):
            if _escapes(call, self_name):
                # The callee can initialize anything it wants from here on.
                return
            if not _is_self_attribute(call.func, self_name):
                continue
            method = _called_method(call, klass)
            if method is None:
                # Unknown method, so unknown attributes: stop here.
                return
            if method is not init:
                yield from _early_accesses(klass, init, call, method, assigned)
                assigned |= _assigned_anywhere(method)
        assigned |= _assigned_attributes(statement, self_name)
        assigned -= _deleted_attributes(statement, self_name)


def _early_accesses(
    klass: nodes.ClassDef,
    init: nodes.FunctionDef,
    call: nodes.Call,
    method: nodes.FunctionDef,
    assigned: set[str],
) -> Iterator[tuple[nodes.Call, str, str, int]]:
    """Yield what *call* reads too early, as (call, method, member, line)."""
    self_name = _self_name(method)
    if self_name is None:
        return
    reported: set[str] = set()
    for attribute in _read_attributes(method, self_name):
        if attribute in assigned or attribute in reported:
            continue
        line = _initialization_line(klass, init, attribute, call.lineno)
        if line is None:
            continue
        reported.add(attribute)
        yield call, method.name, attribute, line


class InitOrderChecker(BaseChecker):
    """Check the order of the statements in ``__init__``.

    Only the statements that always run are considered: the walk stops at the
    first ``if``, loop or ``try``, and at the first call the instance is handed
    over to. Called methods are inspected one call deep. A subclass overriding
    one of them is no reason to stay quiet: the class is broken on its own.
    """

    name = "init-order"
    msgs = {
        "E3901": (
            "Call to %r accesses member %r before it is initialized on line %s",
            "access-member-before-initialization",
            "Used when the constructor calls a method reading an instance "
            "attribute that the constructor only assigns later. The attribute "
            "does not exist yet when the method runs, so building the object "
            "raises an AttributeError.",
        )
    }

    @only_required_for_messages("access-member-before-initialization")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if node.name != "__init__":
            return
        klass = node.parent
        if not isinstance(klass, nodes.ClassDef):
            return
        self_name = _self_name(node)
        if self_name is None:
            return
        found = list(_find_early_accesses(klass, node, self_name))
        # Only now that there is something to say is it worth paying for the
        # ancestors of the class.
        if found and _is_analysable(klass):
            for call, method_name, attribute, line in found:
                self.add_message(
                    "access-member-before-initialization",
                    node=call,
                    args=(method_name, attribute, line),
                    confidence=HIGH,
                )


def _is_analysable(klass: nodes.ClassDef) -> bool:
    """Whether the attributes of *klass* can be tracked by plain assignments."""
    try:
        if klass.declared_metaclass() is not None:
            return False
        ancestors = list(klass.ancestors())
    except astroid.AstroidError:
        return False
    for defined in (klass, *ancestors):
        if not isinstance(defined, nodes.ClassDef):
            return False
        if defined.root().name == "builtins":
            continue
        if DYNAMIC_ATTRIBUTE_METHODS.intersection(defined.locals):
            return False
    return not any(
        attribute.attrname == "__dict__"
        for attribute in klass.nodes_of_class((nodes.Attribute, nodes.AssignAttr))
    )


def _called_method(call: nodes.Call, klass: nodes.ClassDef) -> nodes.FunctionDef | None:
    """Return the method *call* runs, if it can be resolved to a single one."""
    try:
        candidates = klass.local_attr(call.func.attrname)
    except astroid.NotFoundError:
        return None
    if len(candidates) != 1:
        return None
    method = candidates[0]
    if not isinstance(method, nodes.FunctionDef) or _self_name(method) is None:
        return None
    return method


def _initialization_line(
    klass: nodes.ClassDef, init: nodes.FunctionDef, attribute: str, lineno: int
) -> int | None:
    """Return the line where ``__init__`` assigns *attribute*, after *lineno*."""
    try:
        klass.local_attr(attribute)
        return None  # A class attribute exists before __init__ runs.
    except astroid.NotFoundError:
        pass
    try:
        next(klass.instance_attr_ancestors(attribute))
        return None  # A parent constructor may have assigned it already.
    except StopIteration:
        pass
    later = [
        assignment.fromlineno
        for assignment in klass.instance_attrs.get(attribute, ())
        if assignment.frame() is init
        and assignment.fromlineno > lineno
        and not isinstance(assignment.statement(), (nodes.AugAssign, nodes.Delete))
    ]
    return min(later) if later else None


def register(linter: PyLinter) -> None:
    linter.register_checker(InitOrderChecker(linter))
