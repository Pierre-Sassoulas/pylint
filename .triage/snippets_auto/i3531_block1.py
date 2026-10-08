"""Demonstrate false positive for no-member."""
from wtforms.form import BaseForm, FormMeta, Form
from wtforms.meta import DefaultMeta


# pylint: disable=too-few-public-methods,missing-function-docstring,missing-class-docstring,too-many-arguments


# This demonstrates the exact error I am seeing:
class BadForm(Form):
    """A class demonstrating the issue that appears when inheriting from `Form`."""

    def do_something_with_data(self):
        return self.data


# This following two classes demonstrate the @property access working without an error.
class ClassWithProperty:
    """A class with a property."""

    @property
    def a_property(self):
        return "this works"


class AccessPropertyOk(ClassWithProperty):
    """A class that accesses a property on its parent."""

    def do_something(self):
        return self.a_property


# It doesn't seem to have anything to do with how many classes deep the inheritance chain is:
class IsItBecauseOfSeveralClassesInTheHierarchy(AccessPropertyOk):

    def something_else(self):
        return self.a_property


# The error doesn't appear when inheriting from the direct parent of `wtforms.forms.Form`:
class BaseFormChild(BaseForm):

    def do_something_with_data(self):
        return self.data


# Ok, so lets try re-implementing the hierarchy from `WTForms`. This
# is basically what is in `wtforms.forms.Form`
class FormWithMetaclassAndMeta(BaseForm, metaclass=FormMeta):

    Meta = DefaultMeta

    def do_something_with_data(self):
        return self.data


# I don't understand why this does not report an error. I can't see
# how this differs from `BadForm` in any material way:
class ChildForm(FormWithMetaclassAndMeta):

    def something(self):
        return self.data
