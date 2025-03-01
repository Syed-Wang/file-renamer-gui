import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.logger import setup_logging

def main():
    # 设置日志记录
    log_file = setup_logging()
    
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用程序的主事件循环
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()