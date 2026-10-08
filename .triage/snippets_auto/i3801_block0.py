from typing import Callable
​
import attr
​
​
def function(value: int) -> None:
    print(value)
​
​
@attr.s(frozen=True)
class A:
    value: int
    outsourced: Callable = function
​
    def execute(self) -> None:
        self.outsourced(self.value)  # E1121 is here
​
​
a = A(1)
a.execute()
