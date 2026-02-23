import yaml
import os
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "defaults": {
                "cloud_model": "anthropic.claude-3-sonnet-latest",
                "local_model": "generic.llama3.2:latest",
                "use_local": False,
            },
            "ollama": {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "timeout": 60,
            },
        }

    def get_model(self, agent_name: str) -> str:
        """获取指定 Agent 的模型"""
        use_local = self.config.get("defaults", {}).get("use_local", False)

        # 优先使用环境变量
        if os.getenv("USE_LOCAL_MODEL", "").lower() == "true":
            use_local = True

        if use_local:
            # 使用本地模型
            if agent_name in self.config.get("agents", {}):
                return self.config["agents"][agent_name].get(
                    "local", self.config["defaults"]["local_model"]
                )
            return self.config["defaults"]["local_model"]
        else:
            # 使用云端模型
            if agent_name in self.config.get("agents", {}):
                return self.config["agents"][agent_name].get(
                    "cloud", self.config["defaults"]["cloud_model"]
                )
            return self.config["defaults"]["cloud_model"]

    def is_using_local(self) -> bool:
        """是否使用本地模型"""
        use_local = self.config.get("defaults", {}).get("use_local", False)
        if os.getenv("USE_LOCAL_MODEL", "").lower() == "true":
            use_local = True
        return use_local

    def get_ollama_config(self) -> Dict[str, Any]:
        """获取 Ollama 配置"""
        return self.config.get(
            "ollama",
            {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "timeout": 60,
            },
        )


# 全局配置实例
config = Config()
