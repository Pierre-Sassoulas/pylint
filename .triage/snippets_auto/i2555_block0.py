import sys

from PyQt5 import QtWidgets


def create_window():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.definitely_not_one_of_its_attributes()
    window.show()

create_window()
