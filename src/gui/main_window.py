import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from core.rename_utils import rename_files
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件重命名工具")
        self.setGeometry(100, 100, 400, 200)

        self.initUI()

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

        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.start_num_label)
        layout.addWidget(self.start_num_input)
        layout.addWidget(self.prefix_label)
        layout.addWidget(self.prefix_input)
        layout.addWidget(self.rename_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.folder_input.setText(folder_path)

    def rename_files(self):
        folder_path = self.folder_input.text()
        start_num = int(self.start_num_input.text())
        prefix = self.prefix_input.text()

        logging.info(f"开始重命名文件: {folder_path}, 起始数字: {start_num}, 前缀: {prefix}")
        rename_files(folder_path, start_num, prefix)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())