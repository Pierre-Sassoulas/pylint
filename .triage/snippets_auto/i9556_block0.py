import sys


def test_invalid_W0125():
    """
    This test demonstrates a false positive for W0640.

    Message emitted:
    Using a conditional statement with a constant value

    Description:
    Emitted when a conditional statement (If or ternary if) uses a constant
    value for its test. This might not be what the user intended to do.
    """

    for i in range(5):
        try:
            sys.exit(i)
        except SystemExit as e:

            # pylint incorrectly thinks that the following conditional uses
            # a constant value
            if e.code:
                print(f"sys.exit() called with argument: {e.code}")
            assert e.code == i
