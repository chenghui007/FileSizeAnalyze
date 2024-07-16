import os
import sys
from decimal import Decimal, ROUND_HALF_UP

from PySide6 import QtWidgets
from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QFileDialog, QApplication, QPushButton, QTableView, QProgressDialog, \
    QVBoxLayout


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        if left.column() == 2:  # 假设第3列（大小）需要进行自定义排序
            if 'MB' in left.data():
                left_data = int(left.data().removesuffix('MB')) * 1024 * 1024
            elif 'KB' in left.data():
                left_data = int(left.data().removesuffix('KB')) * 1024
            else:
                left_data = int(left.data())
            if 'MB' in right.data():
                right_data = int(right.data().removesuffix('MB')) * 1024 * 1024
            elif 'KB' in right.data():
                right_data = int(right.data().removesuffix('KB')) * 1024
            else:
                right_data = int(right.data())

            return left_data < right_data
        else:
            return super().lessThan(left, right)


class MyWidgets(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 设置窗口信息
        self.setWindowTitle('文件大小分析')
        self.resize(800, 600)
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
        self.layout = QVBoxLayout()
        # 创建文件获取按钮
        self.button_1 = QPushButton("选择文件", self)

        self.layout.addWidget(self.button_1)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)
        self.button_1.clicked.connect(self.open_folder_dialog)
        self.table_view.doubleClicked.connect(self.on_double_click)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.load_data_from_folder(folder_path)

    def load_data_from_folder(self, folder_path):
        self.model.setRowCount(0)

        total_items = len(os.listdir(folder_path)) + 1
        # 创建进度条遮挡
        progress_dialog = QProgressDialog("正在加载文件夹...", "取消", 0, total_items, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle('读取数据')
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)

        current_item = 0
        # row = [self.get_file_icon(1, '..'), self.get_table_row_item('文件夹'),
        #        self.get_table_row_item(''),
        #        self.get_table_row_item(folder_path)
        #        ]
        # self.model.appendRow(row)

        with os.scandir(folder_path) as it:
            for entry in it:
                if progress_dialog.wasCanceled():
                    break
                if entry.is_dir():
                    dir_size = self.get_folder_size(entry.path)
                    row = [self.get_file_icon(1, entry.name), self.get_table_row_item('文件夹'),
                           self.get_table_row_item(str(dir_size) + ' MB'),
                           self.get_table_row_item(entry.path)
                           ]
                else:
                    file_size = Decimal(os.path.getsize(entry.path) / 1024).quantize(Decimal('0'),
                                                                                     rounding=ROUND_HALF_UP)
                    row = [self.get_file_icon(2, entry.name),
                           self.get_table_row_item('文件'),
                           self.get_table_row_item(str(file_size) + ' KB'),
                           self.get_table_row_item(entry.path)
                           ]

                self.model.appendRow(row)
                current_item += 1
                progress_dialog.setValue(current_item)

        self.adjust_colunm_width()
        progress_dialog.close()

    def get_table_row_item(self, name):
        row = QStandardItem(name)
        row.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁用编辑
        return row

    def get_file_icon(self, file_type, name):
        if file_type == 1:
            icon = QIcon('./image/fodler.svg')
            item = QStandardItem(icon, name)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁用编辑
            item.setData('1', Qt.UserRole)
            return item
        elif file_type == 2:
            icon = QIcon('./image/file.svg')
            item = QStandardItem(icon, name)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 禁用编辑
            item.setData('2', Qt.UserRole)
            return item
        return name

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return Decimal(total_size / 1024 / 1024).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

    def resizeEvent(self, event):
        self.adjust_colunm_width()

    def adjust_colunm_width(self):
        total_width = self.width()
        colunms = [20, 10, 10, 56]
        for column in range(0, len(colunms)):
            column_width = total_width / 100 * colunms[column]
            self.table_view.setColumnWidth(column, column_width)

    def on_double_click(self, index: QModelIndex):
        if not index.isValid():
            return
        if index.column() == 0:
            item = self.model.itemFromIndex(self.proxy_model.mapToSource(index))
            if item and item.text():
                folder_path = self.model.item(index.row(), 3).text()
                if os.path.isdir(folder_path):
                    print(f"folder_path is {folder_path}")
                    self.load_data_from_folder(folder_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidgets()
    window.show()
    sys.exit(app.exec())
