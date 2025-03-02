import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
    QHeaderView,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.rename_utils import rename_files, validate_inputs, natural_sort_key
from core.config_manager import ConfigManager
import logging
import traceback
import os


class RenameWorker(QThread):
    """重命名工作线程"""

    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, folder_path, start_num, prefix):
        super().__init__()
        self.folder_path = folder_path
        self.start_num = start_num
        self.prefix = prefix

    def run(self):
        try:
            # 只调用一次rename_files即可
            rename_files(self.folder_path, self.start_num, self.prefix)
            self.progress.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def get_files(self):
        return [
            f
            for f in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, f))
        ]

    def rename_single_file(self, file, index):
        rename_files(self.folder_path, self.start_num + index, self.prefix)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件重命名工具")
        self.setGeometry(100, 100, 400, 200)
        self.config_manager = ConfigManager()

        self.initUI()

        # 加载最近使用的配置
        self.load_recent_config()

    def initUI(self):
        layout = QVBoxLayout()

        self.folder_label = QLabel("文件夹路径:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("浏览")
        self.browse_button.clicked.connect(self.browse_folder)

        self.start_num_label = QLabel("起始数字:")
        self.start_num_input = QLineEdit("1")

        self.prefix_label = QLabel("文件名前缀:")
        self.prefix_input = QLineEdit()

        self.rename_button = QPushButton("开始重命名")
        self.rename_button.clicked.connect(self.rename_files)

        # 添加预览表格
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # 添加预览按钮
        self.preview_button = QPushButton("预览")
        self.preview_button.clicked.connect(self.preview_rename)

        # 添加撤销按钮
        self.undo_button = QPushButton("撤销")
        self.undo_button.clicked.connect(self.undo_rename)

        # 更新布局
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.start_num_label)
        layout.addWidget(self.start_num_input)
        layout.addWidget(self.prefix_label)
        layout.addWidget(self.prefix_input)
        layout.addWidget(self.rename_button)
        layout.addWidget(self.preview_button)
        layout.addWidget(self.preview_table)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.undo_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.folder_input.setText(folder_path)

    def rename_files(self):
        try:
            folder_path = self.folder_input.text().strip()
            start_num = self.start_num_input.text().strip()
            prefix = self.prefix_input.text().strip()

            # 验证输入
            validate_inputs(folder_path, start_num, prefix)

            # 执行重命名
            self.progress_bar.setVisible(True)
            self.worker = RenameWorker(folder_path, int(start_num), prefix)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.finished.connect(self.on_rename_finished)
            self.worker.error.connect(self.on_rename_error)
            self.worker.start()

            # 保存当前配置
            self.save_current_config()

            QMessageBox.information(self, "成功", "文件重命名完成！")

        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
        except Exception as e:
            QMessageBox.critical(
                self, "错误", f"发生错误：{str(e)}\n{traceback.format_exc()}"
            )

    def preview_rename(self):
        """预览重命名结果"""
        try:
            folder_path = self.folder_input.text().strip()
            start_num = int(self.start_num_input.text().strip())
            prefix = self.prefix_input.text().strip()

            files = [
                f
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
            files.sort(key=natural_sort_key)

            self.preview_table.setRowCount(len(files))
            self.preview_table.setUpdatesEnabled(False)
            for i, file in enumerate(files):
                if prefix:
                    # 如果有前缀，使用 "数字-前缀.扩展名" 格式
                    _, ext = os.path.splitext(file)
                    new_name = f"{i + start_num}-{prefix}{ext}"
                else:
                    # 如果没有前缀，使用 "数字-原文件名" 格式
                    new_name = f"{i + start_num}-{file}"

                self.preview_table.setItem(i, 0, QTableWidgetItem(file))
                self.preview_table.setItem(i, 1, QTableWidgetItem(new_name))
            self.preview_table.setUpdatesEnabled(True)

        except Exception as e:
            QMessageBox.warning(self, "预览错误", str(e))

    def load_recent_config(self):
        """加载最近使用的配置"""
        config = self.config_manager.config
        if config["recent_folders"]:
            self.folder_input.setText(config["recent_folders"][-1])
        if config["recent_prefixes"]:
            self.prefix_input.setText(config["recent_prefixes"][-1])
        self.start_num_input.setText(str(config["last_start_num"]))

    def save_current_config(self):
        """保存当前配置"""
        config = self.config_manager.config

        # 保存最近的文件夹
        folder = self.folder_input.text().strip()
        if folder and folder not in config["recent_folders"]:
            config["recent_folders"].append(folder)
            config["recent_folders"] = config["recent_folders"][-5:]  # 只保留最近5个

        # 保存最近的前缀
        prefix = self.prefix_input.text().strip()
        if prefix and prefix not in config["recent_prefixes"]:
            config["recent_prefixes"].append(prefix)
            config["recent_prefixes"] = config["recent_prefixes"][-5:]

        config["last_start_num"] = int(self.start_num_input.text().strip())

        self.config_manager.save_config()

    def undo_rename(self):
        """撤销重命名"""
        if self.config_manager.undo_last_rename():
            QMessageBox.information(self, "成功", "已撤销最近一次重命名操作")
        else:
            QMessageBox.warning(self, "错误", "没有可撤销的操作")

    def closeEvent(self, event):
        self.save_current_config()
        super().closeEvent(event)

    def on_rename_finished(self):
        """重命名完成时的回调"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

    def on_rename_error(self, error_message):
        """重命名出错时的回调"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "错误", f"重命名过程中发生错误：{error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
