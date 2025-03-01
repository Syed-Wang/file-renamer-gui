import os
import logging
from datetime import datetime

def setup_logging():
    """
    设置日志配置
    """
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 在脚本所在目录下创建logs文件夹
    logs_dir = os.path.join(script_dir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 生成日志文件名，包含时间戳
    log_filename = os.path.join(logs_dir, f"file_renamer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    return log_filename