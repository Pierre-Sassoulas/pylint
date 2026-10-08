from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSpinBox, QComboBox, QLabel

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 72)
        self.font_size.setValue(12)
        layout.addWidget(self.font_size)

        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System"])
        layout.addWidget(self.theme)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

        # these trigger E1136
        self.font_size.valueChanged[int].connect(self.on_font_changed)
        self.theme.currentIndexChanged[int].connect(self.on_theme_changed)

    def on_font_changed(self, size):
        self.status.setText(f"Font size: {size}pt")

    def on_theme_changed(self, index):
        self.status.setText(f"Theme: {self.theme.itemText(index)}")

if __name__ == "__main__":
    app = QApplication([])
    panel = SettingsPanel()
    panel.show()
    app.exec()
