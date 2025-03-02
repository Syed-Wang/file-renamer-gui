import json
import os
import logging
from datetime import datetime  # save_history 方法中使用但未导入


class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.history_file = os.path.join(os.path.dirname(__file__), "history.json")
        self.load_config()

    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
        except json.JSONDecodeError:
            logging.error("配置文件格式错误")
            self.config = self._get_default_config()
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
            self.config = self._get_default_config()

    def save_config(self):
        """保存配置"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def save_history(self, old_names, new_names, folder_path):
        """保存重命名历史"""
        history = {
            "folder_path": folder_path,
            "old_names": old_names,
            "new_names": new_names,
            "timestamp": datetime.now().isoformat(),
        }

        histories = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                histories = json.load(f)

        histories.append(history)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(histories, f, ensure_ascii=False, indent=2)

    def undo_last_rename(self):
        """撤销最后一次重命名"""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                histories = json.load(f)

            if histories:
                last_history = histories.pop()
                folder_path = last_history["folder_path"]

                # 执行撤销
                for old_name, new_name in zip(
                    last_history["old_names"], last_history["new_names"]
                ):
                    old_path = os.path.join(folder_path, old_name)
                    new_path = os.path.join(folder_path, new_name)
                    if os.path.exists(new_path):
                        os.rename(new_path, old_path)

                # 保存更新后的历史
                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump(histories, f, ensure_ascii=False, indent=2)

                return True
        return False

    def _get_default_config(self):
        """返回默认配置"""
        return {
            "recent_folders": [],
            "recent_prefixes": [],
            "last_start_num": 1
        }
