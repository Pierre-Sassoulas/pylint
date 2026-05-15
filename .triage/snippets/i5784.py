def example_decorator(*new_func_args, **new_func_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print_me = kwargs.pop("print_me", None)

            def inner(*inner_args, **inner_kwargs):
                print(print_me)
                return func(*inner_args, **inner_kwargs)

            return inner(*args, **kwargs)

        return wrapper

    if (
        len(new_func_args) == 1
        and len(new_func_kwargs) == 0
        and callable(new_func_args[0])
    ):
        return decorator(new_func_args[0])
    return decorator


@example_decorator
def example_func(num):
    return num**2


example_func(6, print_me="hello")
