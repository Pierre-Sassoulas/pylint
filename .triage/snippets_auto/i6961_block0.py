class HasWhoAmI:
    def whoami(self):
        pass

class ClassB(HasWhoAmI):
    def whoami(self):
        super().whoami()

class ClassC(HasWhoAmI):
    def whoami(self):
        super().whoami()

class ClassD(ClassB, ClassC):
    def greet(self):
        super(ClassB, self).whoami()  # previously raised
