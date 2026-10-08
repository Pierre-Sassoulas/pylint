"""False-positive 'inconsistent MRO'."""
from pathlib import Path
from typing import Protocol

from PySide6.QtWidgets import QApplication, QMainWindow


class Appear(Protocol):
    def appear(self) -> None:
        ...


# Here, we get a false-positive "inconsistent MRO" in `pylint` ...
class WindowMeta(type(QMainWindow), type(Appear)):
    pass

class MyWindow(QMainWindow, Appear, metaclass=WindowMeta):
    def appear(self) -> None:
        self.show()

# ... as evidenced by this code working fine in `python`:
application = QApplication()
my_window = MyWindow()
my_window.appear()
application.exec()


# By contrast, this "inconsistent MRO" error in `pylint` ...
class PathMeta(type(Path), type(Appear)):
    pass

class MyPath(Path, Appear, metaclass=PathMeta):
    def appear(self) -> None:
        print(self)

# ... matches the (failing) behavior in `python`:
my_path = MyPath()
my_path.appear()
