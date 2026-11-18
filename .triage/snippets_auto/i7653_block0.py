# save as test.py
class a():
    x: str = ''

class b():
    y: a = a()

class c():
    z: list[b] = [b()]
    z.append(b())
