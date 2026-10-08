class ClassWithMember:
     """Member defined in superclass."""
     def __init__(self):
         if False:
             self.member = True

class AssignMemberFromSuper(ClassWithMember):
     """This assignment is valid due to inheritance."""
     def __init__(self):
         super().__init__()
         self.member = self.member
