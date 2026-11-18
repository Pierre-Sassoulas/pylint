def hello(who):
    """Override argument without using it"""
    who = "world"
    print(who)

def foobar():
    """Override variable value without using it"""
    quux = "a"
    quux = "b"
    return quux
