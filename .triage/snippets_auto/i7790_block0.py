# pylint: disable = missing-function-docstring, missing-class-docstring, missing-module-docstring, 
# pylint: disable = too-many-function-args, too-many-instance-attributes, invalid-name, 
# pylint: disable = too-many-arguments, too-many-lines

from dataclasses import dataclass

@dataclass(slots=True)
class Aaa:
    def __init__(self):
        self.x = 1

a = Aaa()
