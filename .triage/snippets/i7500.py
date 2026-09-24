import types

code = compile("pass", "<stdin>", "exec")
types.FunctionType(code, {})()
