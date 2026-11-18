import astroid

def register(_):
    pass

def _transform(_):
    return astroid.parse("""
class Hello(object):
    def __init__(self):
        self.x = 1
        self.y = 2
""")

def _looks_like_hello(node):
    return node.qname() == "hello"

astroid.MANAGER.register_transform(astroid.Module, _transform, _looks_like_hello)
