def example(arg_a='a', arg_b='b'):  # unused-argument
    """An example function."""
    var_c = 'c'  # potentially-unused-variable
    return locals()  # {'arg_a': 'a', 'arg_b': 'b', 'var_c': 'c'}
