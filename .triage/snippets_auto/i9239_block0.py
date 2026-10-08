# file a.py
from typing import Callable, Union

class A:
   def do_stuff(self, data: bytes) -> Union[None, str]:
       for map_name, x_function in self.x_functions.items():
           return x_function(self, data)

   def funct_1(self, data: bytes) -> None:
       # something
       return None

   def funct_2(self, data: bytes) -> str:
       return str(bytes)

   x_functions: dict[str, Callable[[Self, bytes], Union[None, str]] = {
       "funct_1": funct_1,
       "funct_2": funct_2
   }
