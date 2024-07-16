import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui





class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("QFormLayout")
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""

        name_le = QtWidgets.QLineEdit(self)
        age_label = QtWidgets.QLabel("年龄：", self)
        age_spinbox = QtWidgets.QSpinBox(self)
        age_spinbox.setRange(1, 150)
        age_spinbox.setValue(20)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("姓名：", name_le)
        layout.addRow(age_label, age_spinbox)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
