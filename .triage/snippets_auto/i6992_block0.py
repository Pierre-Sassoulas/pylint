class A:
   def close(self):
      print('A')

class B:
   def close(self):
      print('B')

class C(A, B):
   def close(self):
      print('C')
      super().close()


C().stop()
