"""Tests for access-member-before-initialization."""
# pylint: disable=missing-docstring, too-few-public-methods


class CallBeforeAssignment:
    def __init__(self):
        self.compute()  # [access-member-before-initialization]
        self.rate = 100

    def compute(self):
        return self.rate * 2


class AugmentedRead:
    def __init__(self):
        self.total = 0
        self.accumulate()  # [access-member-before-initialization]
        self.rate = 100

    def accumulate(self):
        self.rate += 1
        self.total += self.rate


class CallInAssignment:
    def __init__(self):
        self.doubled = self.compute()  # [access-member-before-initialization]
        self.rate = 100

    def compute(self):
        return self.rate * 2


class SeveralAttributes:
    def __init__(self):
        self.compute()  # [access-member-before-initialization,access-member-before-initialization]
        self.rate = 100
        self.count = 2

    def compute(self):
        return self.rate * self.count


class CallAfterAssignment:
    def __init__(self):
        self.rate = 100
        self.compute()

    def compute(self):
        return self.rate * 2


class ClassAttributeDefault:
    rate = 1

    def __init__(self):
        self.compute()
        self.rate = 100

    def compute(self):
        return self.rate * 2


class ParentAssigns:
    def __init__(self):
        self.rate = 1


class ChildReassigns(ParentAssigns):
    def __init__(self):
        super().__init__()
        self.compute()
        self.rate = 100

    def compute(self):
        return self.rate * 2


class GuardedRead:
    def __init__(self):
        self.compute()
        self.rate = 100

    def compute(self):
        if hasattr(self, "rate"):
            return self.rate * 2
        return 0


class AssignedElsewhere:
    def __init__(self):
        self.compute()  # [access-member-before-initialization]
        self.rate = 100

    def prepare(self):
        self.rate = 1

    def compute(self):
        return self.rate * 2


class HelperAssigns:
    def __init__(self):
        self.prepare()
        self.compute()
        self.rate = 100

    def prepare(self):
        self.rate = 1

    def compute(self):
        return self.rate * 2


class CallsAnAttribute:
    def __init__(self, callback):
        self.callback = callback
        self.callback()
        self.rate = 100


class HandsOverSelf:
    def __init__(self):
        setattr(self, "rate", 1)
        self.compute()
        self.rate = 100

    def compute(self):
        return self.rate * 2


class DynamicAttributes:
    def __init__(self):
        self.compute()
        self.rate = 100

    def __getattr__(self, name):
        return 0

    def compute(self):
        return self.rate * 2


class CallInCondition:
    def __init__(self, ready):
        if ready:
            self.compute()
        self.rate = 100

    def compute(self):
        return self.rate * 2


class ParentDefinesMethod:
    def compute(self):
        return self.rate * 2  # [no-member]


class InheritedMethod(ParentDefinesMethod):
    def __init__(self):
        self.compute()  # [access-member-before-initialization]
        self.rate = 100


class NeverAssigned:
    def __init__(self):
        self.compute()

    def compute(self):
        return self.rate * 2  # [no-member]


class MethodAssignsFirst:
    def __init__(self):
        self.compute()
        self.rate = 100

    def compute(self):
        self.rate = 1
        return self.rate * 2


class DecoratedMethod:
    def __init__(self):
        self.compute()
        self.rate = 100

    @staticmethod
    def compute():
        return 2


class DunderDict:
    def __init__(self):
        self.__dict__["rate"] = 1
        self.compute()
        self.rate = 100

    def compute(self):
        return self.rate * 2
