code = """
def function():
    x = 10
    del x
    print(x)
"""
import astroid
ast = astroid.parse(code)
n = [n for n in ast.nodes_of_class(astroid.Name) if n.name == "x"][0]
print(n.lookup('x'))  # Correctly doesn't return any AssignNames
