class Y:
    def other(self) -> Y:  # false-positive undefined-variable
        return self
