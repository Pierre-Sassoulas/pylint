if str is bytes:

    class C:
        def __init__(self, a):
            pass

else:

    class C:
        def __init__(self, a, b):
            pass


C(1, b=2)
