class TestPylint_return_1:
    def foo(self) -> bool:
        return self.bool()

    def bool(self) -> bool:
        return True
