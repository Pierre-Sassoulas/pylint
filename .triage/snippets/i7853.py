def get_func(param):
    if param is None:

        def func():
            return None

    else:

        def func():
            return param

    return func


def process_val(param):
    func = get_func(param)
    val = func()
    return val
