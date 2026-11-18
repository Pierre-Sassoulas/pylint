class MyClass:
    def __init__(self) -> None:
        self.attribute = [1, 2, 3]

   def my_other_method(self):
        """This should raise as we are appending."""
        for var in self.attribute:
            self.attribute.append(var)  # [modified-iterating-list]
