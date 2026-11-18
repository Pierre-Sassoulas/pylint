from mymodule.myclasses import ClassA

class ClassB:
    badClassVariable = 0

example_a = ClassA()
example_a.badClassVariable = 1  # pylint: disable=invalid-name

example_b = ClassB()
example_b.badClassVariable = 1  # pylint: disable=invalid-name

badVariable = 1  # pylint: disable=invalid-name

