from PySide6.QtWidgets import QApplication, QSlider

from __feature__ import snake_case, true_property  # isort: skip

QApplication()
slider = QSlider()
print(slider.maximum)
print(slider.maximum == 99)
