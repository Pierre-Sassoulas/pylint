class Any:
    def func(self):
        var = super().func()
        return [_ for _ in var]
