"""Test module that defines a name that will be redefined
in the demo module.
"""
import demo

def test_demo():
    """Test function that defines the outer name"""
    demo.some_redefined_variable = "something"
    demo.main()
