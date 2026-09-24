def func(arg):
    print(arg)


d = {"b": "hello world"}
d["arg"] = d["b"]
del d["b"]

func(**d)
