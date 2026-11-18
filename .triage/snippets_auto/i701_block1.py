#!python

class A:
   def __init__(self):
      self.value = None
   def foo(self):
      return self.value[some_key]

class B(A):
   def __init__(self):
       super(B, self).__init__()
       self.value = [1, 2, 3]
