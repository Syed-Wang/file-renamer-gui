import os
import re
import logging

def natural_sort_key(s):
    """
    自然排序的键函数
    将字符串中的数字部分转换为整数进行比较
    """
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split("([0-9]+)", s)
    ]

def rename_files(path, start_num=1, prefix=""):
    """
    重命名指定文件夹下的所有文件
    :param path: 文件夹路径
    :param start_num: 起始数字，默认为1
    :param prefix: 文件名前缀，默认为空
    """
    # 确保路径存在
    if not os.path.exists(path):
        logging.error(f"路径 {path} 不存在!")
        return

    # 获取所有文件
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # 使用自然排序
    files.sort(key=natural_sort_key)

    # 记录处理的文件总数
    total_files = len(files)
    successful_renames = 0
    failed_renames = 0

    # 遍历并重命名文件
    for index, file in enumerate(files, start=start_num):
        # 获取文件扩展名
        _, ext = os.path.splitext(file)
        # 构建新文件名
        new_name = f"{index}-{prefix}{ext}"
        # 构建完整的文件路径
        old_file = os.path.join(path, file)
        new_file = os.path.join(path, new_name)

        try:
            os.rename(old_file, new_file)
            logging.info(f"已重命名: {file} -> {new_name}")
            successful_renames += 1
        except Exception as e:
            logging.error(f"重命名 {file} 时出错: {str(e)}")
            failed_renames += 1

    # 记录总结信息
    logging.info("-" * 50)
    logging.info(f"重命名操作完成:")
    logging.info(f"总文件数: {total_files}")
    logging.info(f"成功: {successful_renames}")
    logging.info(f"失败: {failed_renames}")
    logging.info("-" * 50)