def lazy(func):
    def wrapped(*args, **kwargs):
        return None

    return wrapped


@lazy
def function(y):
    return y


has_an_error = function("this line has E1111")
print(has_an_error)
