def func():
    class X:
        def other(self) -> X:  # false-positive undefined-variable
            return self
