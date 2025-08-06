#!/usr/bin/env python3
"""
AI 研究助手启动脚本
基于 fast-agent 构建的智能研究原型系统
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_agent.main import main

if __name__ == "__main__":
    print("启动 AI 研究助手...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已中断")
    except Exception as e:
        print(f"启动失败: {e}")
        print("请确保已安装所需依赖并配置了 API 密钥")