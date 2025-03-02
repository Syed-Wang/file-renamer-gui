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


def validate_inputs(path, start_num, prefix):
    """验证输入参数"""
    if not os.path.exists(path):
        raise ValueError("文件夹路径不存在")

    if not os.path.isdir(path):
        raise ValueError("指定路径不是文件夹")

    try:
        start_num = int(start_num)
        if start_num < 0:
            raise ValueError("起始数字必须大于等于0")
    except ValueError:
        raise ValueError("起始数字必须是有效的整数")

    if len(prefix) > 50:
        raise ValueError("前缀长度不能超过50个字符")

    return True


def rename_files(path, start_num=1, prefix=""):
    """
    重命名指定文件夹下的所有文件
    :param path: 文件夹路径
    :param start_num: 起始数字，默认为1
    :param prefix: 文件名前缀，默认为空。如果为空，则在原文件名前添加数字前缀
    """
    # 验证输入参数
    validate_inputs(path, start_num, prefix)

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
        try:
            if prefix:
                # 如果有前缀，使用 "数字-前缀.扩展名" 格式
                _, ext = os.path.splitext(file)
                new_name = f"{index}-{prefix}{ext}"
            else:
                # 如果没有前缀，使用 "数字-原文件名" 格式
                new_name = f"{index}-{file}"
                
            old_file = os.path.join(path, file)
            new_file = os.path.join(path, new_name)

            if os.path.exists(new_file):
                base, ext = os.path.splitext(new_name)
                counter = 1
                while os.path.exists(os.path.join(path, f"{base}_{counter}{ext}")):
                    counter += 1
                new_name = f"{base}_{counter}{ext}"
                new_file = os.path.join(path, new_name)

            try:
                os.rename(old_file, new_file)
            except OSError as e:
                logging.error(f"重命名失败 {file}: {e.strerror}")
            except PermissionError:
                logging.error(f"没有权限重命名文件 {file}")
            else:
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
