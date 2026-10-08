def function(*args):
    print(args)

def wrapper(arg):
    return lambda *args: function(arg, *args)

if __name__ == "__main__":
    args = None
    func = wrapper(1)
    func(2)
