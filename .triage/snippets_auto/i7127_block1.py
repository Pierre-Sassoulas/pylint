class HasClose:
    def close(self):
        """Example demonstrating better inheritance pattern"""


class Child6(HasClose):
    def close(self):
        print("Child6")
        super().close()


class Child7(HasClose):
    def close(self):
        print("Child7")
        super().close()


class Grandchild(Child6, Child7):
    def close(self):
        """All paths delegate to super -- no warning"""
        print("Grandchild")
        super().close()
