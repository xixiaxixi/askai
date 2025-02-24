import json
import os
from pathlib import Path
from platformdirs import user_config_dir

class ConfigManager:
    """
    Configuration:
    Configurations are stored in:
    - Linux: ~/.config/askai/config.json
    - macOS: ~/Library/Application Support/askai/config.json
    - Windows: %LOCALAPPDATA%\\askai\\config.json
    """
    def __init__(self):
        self.config_dir = Path(user_config_dir("askai"))
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self):
        """加载配置"""
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_config(self, config):
        """保存配置"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def set_api_key(self, api_key):
        """设置 API Key"""
        config = self.load_config()
        config['api_key'] = api_key
        self.save_config(config)

    def set_base_url(self, base_url):
        """设置 Base URL"""
        config = self.load_config()
        config['base_url'] = base_url
        self.save_config(config)

    def get_api_key(self):
        """获取 API Key"""
        config = self.load_config()
        return config.get('api_key')

    def get_base_url(self):
        """获取 Base URL"""
        config = self.load_config()
        return config.get('base_url')