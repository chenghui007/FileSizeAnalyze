import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QApplication, QPushButton, QBoxLayout, QTableView, QProgressDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        if left.column() == 2:  # 假设第3列（大小）需要进行自定义排序
            left_data = int(left.data())
            right_data = int(right.data())
            return left_data < right_data
        else:
            return super().lessThan(left, right)


class MyWidgets(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 设置窗口信息
        self.setWindowTitle('文件大小分析')
        self.resize(500, 600)
        # 创建表格视图
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['名称', '类型', '大小 (字节)', '路径'])
        self.proxy_model = MySortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        # 将模型设置到表格视图
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        # 创建layout布局
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        # 创建文件获取按钮
        self.button_1 = QPushButton("选择文件", self)
        self.layout.addWidget(self.button_1)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)
        self.button_1.clicked.connect(self.open_folder_dialog)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.load_data_from_folder(folder_path)

    def load_data_from_folder(self, folder_path):
        self.model.setRowCount(0)

        # 获取文件和文件夹的总数
        total_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(folder_path)])

        # 创建进度对话框
        progress_dialog = QProgressDialog("正在加载文件夹...", "取消", 0, total_items, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)

        current_item = 0

        for root, dirs, files in os.walk(folder_path):
            for name in dirs:
                if progress_dialog.wasCanceled():
                    break
                dir_path = os.path.join(root, name)
                dir_size = self.get_folder_size(dir_path)
                row = [QStandardItem(name), QStandardItem('文件夹'), QStandardItem(str(dir_size)),
                       QStandardItem(dir_path)]
                self.model.appendRow(row)
                current_item += 1
                progress_dialog.setValue(current_item)

            for name in files:
                if progress_dialog.wasCanceled():
                    break
                file_path = os.path.join(root, name)
                file_size = os.path.getsize(file_path)
                row = [QStandardItem(name), QStandardItem('文件'), QStandardItem(str(file_size)),
                       QStandardItem(file_path)]
                self.model.appendRow(row)
                current_item += 1
                progress_dialog.setValue(current_item)

            if progress_dialog.wasCanceled():
                break

        progress_dialog.close()

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidgets()
    window.show()
    sys.exit(app.exec())
