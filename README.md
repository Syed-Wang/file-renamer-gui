# 文件重命名器 GUI

## 项目简介

这个项目是一个图形化的文件重命名工具，允许用户通过简单的界面批量重命名文件。用户可以指定文件夹路径、起始数字和文件名前缀。

## 文件结构

``` plaintext
file-renamer-gui
├── src
│   ├── main.py                # 应用程序的入口点
│   ├── gui
│   │   └── main_window.py     # 图形用户界面的主窗口
│   ├── core
│   │   ├── rename_utils.py    # 文件重命名的工具函数
│   │   └── logger.py          # 日志记录设置
│   └── resources
│       └── style.qss          # GUI 的样式表
├── requirements.txt           # 项目依赖
└── README.md                  # 项目文档
```

## 安装依赖

在项目根目录下运行以下命令以安装所需的依赖：

``` bash
pip install -r requirements.txt
```

## 运行应用

使用以下命令启动应用程序：

``` bash
python src/main.py
```

## 使用说明

1. 输入文件夹路径。
2. 输入起始数字（默认为 1）。
3. 输入文件名前缀（可选）。
4. 点击“开始重命名”按钮。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。
