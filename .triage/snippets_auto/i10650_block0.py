from PySide6.QtWidgets import QApplication, QPushButton

app = QApplication()
button = QPushButton()
button.clicked.connect(quit)
button.show()
app.exec()
