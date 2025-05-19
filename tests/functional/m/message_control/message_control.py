"""Test for message control (enable/disable the regex to match messages)."""

# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods


from typing import NamedTuple


class OnlyBlip(NamedTuple):
    blip = True


# Module level controls
print(OnlyBlip().blip)
print(OnlyBlip().module_level_error)  # [no-member]
# pylint: disable=no-member
print(OnlyBlip().module_level_disabled)
# pylint: enable=no-member
print(OnlyBlip().module_level_reenabled)  # [no-member]
print(OnlyBlip().inline_disable)  # pylint: disable=no-member
# pylint: disable-next=no-member
print(OnlyBlip().inline_disabled_next)


def function_globally_enabled():
    print(OnlyBlip().function_level_error)  # [no-member]
    # pylint: disable=no-member
    print(OnlyBlip().function_level_disabled)
    # pylint: enable=no-member
    print(OnlyBlip().function_level_reenabled)  # [no-member]


# pylint: disable=no-member
def function_globally_disabled():
    print(OnlyBlip().function_level_error)
    # pylint: enable=no-member
    print(OnlyBlip().function_level_reenabled)  # [no-member]
    # pylint: disable=no-member
    print(OnlyBlip().function_level_disabled)


# pylint: enable=no-member
def function_scope_disabled():  # pylint: disable=no-member
    # known false positive when function scope disabled
    print(OnlyBlip().function_level_error)  # [no-member]
    # pylint: enable=no-member
    print(OnlyBlip().function_level_reenabled)  # [no-member]
    # pylint: disable=no-member
    print(OnlyBlip().function_level_disabled)


# pylint: disable=no-member
def function_scope_enabled():  # pylint: enable=no-member
    print(OnlyBlip().function_level_error)  # known false negative when function scope enabled
    # pylint: disable=no-member
    print(OnlyBlip().function_level_disabled)
    # pylint: enable=no-member
    print(OnlyBlip().function_level_reenabled)  # [no-member]


# pylint: enable=no-member
class ClassGloballyEnabled:
    class_level_blip = OnlyBlip().blip
    class_level_error = OnlyBlip().class_level_error  # [no-member]
    # pylint: disable=no-member
    class_level_disabled = OnlyBlip().class_level_disabled
    # pylint: enable=no-member
    class_level_reenabled = OnlyBlip().class_level_reenabled  # [no-member]

    def method(self):
        print(OnlyBlip().method_level_error)  # [no-member]
        # pylint: disable=no-member
        print(OnlyBlip().method_level_disabled)
        # pylint: enable=no-member
        print(OnlyBlip().method_level_reenabled)  # [no-member]

    def if_else_control(self):
        condition = True
        if condition:
            print(OnlyBlip().if_block_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in if
            print(OnlyBlip().if_block_disabled)
            # pylint: enable=no-member
        else:
            print(OnlyBlip().else_block_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in else
            print(OnlyBlip().else_block_disabled)
            # pylint: enable=no-member

        # Verify block-level disables don't leak outside their blocks
        print(OnlyBlip().after_if_else_blocks)  # [no-member]

    def loop_control(self):
        # For loop with message control
        print(OnlyBlip().before_for_loop)  # [no-member]
        for _ in range(3):
            print(OnlyBlip().for_loop_start_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in loop
            print(OnlyBlip().for_loop_disabled)
            # pylint: enable=no-member
            print(OnlyBlip().for_loop_end_error)  # [no-member]

        # Outside loop - disable no longer applies
        print(OnlyBlip().after_for_loop)  # [no-member]

        # While loop with message control
        count = 0
        print(OnlyBlip().before_while_loop)  # [no-member]
        while count < 3:
            print(OnlyBlip().while_loop_start_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in while
            print(OnlyBlip().while_loop_disabled)
            # pylint: enable=no-member
            print(OnlyBlip().while_loop_end_error)  # [no-member]
            count += 1

        # Outside while - disable no longer applies
        print(OnlyBlip().after_while_loop)  # [no-member]

    def try_except_control(self):
        print(OnlyBlip().before_try_block)  # [no-member]
        try:
            print(OnlyBlip().try_block_start_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in try
            print(OnlyBlip().try_block_disabled)
            # pylint: enable=no-member
            print(OnlyBlip().try_block_end_error)  # [no-member]
        except ZeroDivisionError:
            print(OnlyBlip().except_block_start_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in except
            print(OnlyBlip().except_block_disabled)
            # pylint: enable=no-member
            print(OnlyBlip().except_block_end_error)  # [no-member]
        finally:
            print(OnlyBlip().finally_block_start_error)  # [no-member]
            # pylint: disable=no-member  # Block-level disable in finally
            print(OnlyBlip().finally_block_disabled)
            # pylint: enable=no-member
            print(OnlyBlip().finally_block_end_error)  # [no-member]

        print(OnlyBlip().after_try_except_finally)  # [no-member]

    def nested_scope_control(self):
        print(OnlyBlip().outer_function_error)  # [no-member]
        # pylint: disable=no-member  # Outer method-level disable
        print(OnlyBlip().outer_function_disabled)

        def inner_function():
            # Still inherits outer disable
            print(OnlyBlip().inner_function_inherited_disable)
            # pylint: enable=no-member  # Enable inside inner function
            print(OnlyBlip().inner_function_reenabled)  # [no-member]
            # pylint: disable=no-member  # Re-disable inside inner function
            print(OnlyBlip().inner_function_disabled)

        inner_function()

        # Outer function still has disables
        print(OnlyBlip().outer_function_still_disabled)
        # pylint: enable=no-member
        print(OnlyBlip().outer_function_reenabled)  # [no-member]


class ClassGloballyDisabled:
    class_level_blip = OnlyBlip().blip
    class_level_error = OnlyBlip().class_level_error  # [no-member]
    # pylint: disable=no-member
    class_level_disabled = OnlyBlip().class_level_disabled
    # pylint: enable=no-member
    class_level_reenabled = OnlyBlip().class_level_reenabled  # [no-member]

    def blop(self):
        print(OnlyBlip().blop)
