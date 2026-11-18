"""Module that redefines a name defined
in an outer scope
"""

def main():
    """This function redefines some_redefined_variable"""
    some_redefined_variable = "something else"
    print(f"{some_redefined_variable}")
