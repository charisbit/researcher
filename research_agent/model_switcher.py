import os
import subprocess
import asyncio
from .config import config

class ModelSwitcher:
    """模型切换器 - 在云端和本地模型之间切换"""
    
    def __init__(self):
        self.config = config
    
    async def check_ollama_status(self) -> bool:
        """检查 Ollama 服务是否运行"""
        try:
            # 检查 Ollama 进程
            result = subprocess.run(
                ["pgrep", "-f", "ollama"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def list_available_models(self) -> dict:
        """列出可用的模型"""
        models = {
            "cloud": [],
            "local": []
        }
        
        # 云端模型（如果有 API 密钥）
        if os.getenv("ANTHROPIC_API_KEY"):
            models["cloud"].extend([
                "anthropic.claude-3-sonnet-latest",
                "anthropic.claude-3-haiku-latest"
            ])
        
        if os.getenv("OPENAI_API_KEY"):
            models["cloud"].extend([
                "openai.gpt-4o",
                "openai.gpt-3.5-turbo"
            ])
        
        # 本地模型（如果 Ollama 运行中）
        if await self.check_ollama_status():
            try:
                result = subprocess.run(
                    ["ollama", "list"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                    for line in lines:
                        if line.strip():
                            model_name = line.split()[0]
                            models["local"].append(f"generic.{model_name}")
            except Exception as e:
                print(f"获取 Ollama 模型列表失败: {e}")
        
        return models
    
    async def switch_to_local(self):
        """切换到本地模型"""
        if await self.check_ollama_status():
            os.environ["USE_LOCAL_MODEL"] = "true"
            print("已切换到本地 Ollama 模型")
            return True
        else:
            print("Ollama 服务未运行，无法切换到本地模型")
            print("请运行: ollama serve")
            return False
    
    async def switch_to_cloud(self):
        """切换到云端模型"""
        os.environ["USE_LOCAL_MODEL"] = "false"
        print("已切换到云端模型")
        return True
    
    def get_current_mode(self) -> str:
        """获取当前模式"""
        return "本地" if self.config.is_using_local() else "云端"
    
    async def auto_detect_best_mode(self) -> str:
        """自动检测最佳模式"""
        # 如果设置了使用本地模型，优先检查 Ollama
        if os.getenv("USE_LOCAL_MODEL", "").lower() == "true":
            if await self.check_ollama_status():
                return "local"
            else:
                print("警告: 配置使用本地模型但 Ollama 未运行，回退到云端模型")
                return "cloud"
        
        # 检查是否有云端 API 密钥
        has_cloud_api = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"))
        
        if not has_cloud_api and await self.check_ollama_status():
            print("未检测到云端 API 密钥，使用本地 Ollama 模型")
            await self.switch_to_local()
            return "local"
        elif has_cloud_api:
            return "cloud"
        else:
            raise RuntimeError(
                "未检测到可用的模型。请配置云端 API 密钥或启动 Ollama 服务。"
            )

# 全局模型切换器实例
model_switcher = ModelSwitcher()