def my_func(this, that):
    return this, that


kwargs = dict(this=1, that=2)
new_kwargs = dict(kwargs, that=3)
my_func(**new_kwargs)
