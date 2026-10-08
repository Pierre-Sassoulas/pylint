class A:
    def func(self, arg1, arg2):
        super().func([arg1, arg2])


class B:
    def func(self, args):
        print(args)


class B(A, B):
    pass
