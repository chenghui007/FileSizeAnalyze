import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PySide6.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("PySide6 表格视图示例")

        # 创建一个中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(central_widget)

        # 创建一个表格视图
        table_view = QTableView()

        # 创建一个标准项模型
        model = QStandardItemModel(4, 3)  # 4 行 3 列
        model.setHorizontalHeaderLabels(['列1', '列2', '列3'])

        # 填充数据
        for row in range(4):
            for column in range(3):
                item = QStandardItem(f"Item {row + 1},{column + 1}")
                model.setItem(row, column, item)

        # 将模型设置到表格视图
        table_view.setModel(model)

        # 将表格视图添加到布局
        layout.addWidget(table_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
