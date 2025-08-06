#!/usr/bin/env python3
"""
Ollama 集成测试脚本
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_agent.config import config
from research_agent.model_switcher import model_switcher

async def test_ollama_integration():
    """测试 Ollama 集成功能"""
    print("=== Ollama 集成测试 ===\n")
    
    # 1. 检查 Ollama 状态
    print("1. 检查 Ollama 服务状态...")
    ollama_running = await model_switcher.check_ollama_status()
    print(f"   Ollama 服务: {'✅ 运行中' if ollama_running else '❌ 未运行'}")
    
    if not ollama_running:
        print("\n请确保 Ollama 服务正在运行:")
        print("   ollama serve")
        return False
    
    # 2. 列出可用模型
    print("\n2. 检查可用模型...")
    models = await model_switcher.list_available_models()
    
    print(f"   云端模型: {len(models['cloud'])} 个")
    for model in models['cloud']:
        print(f"     - {model}")
    
    print(f"   本地模型: {len(models['local'])} 个")
    for model in models['local']:
        print(f"     - {model}")
    
    if not models['local']:
        print("\n❌ 未找到本地模型，请下载模型:")
        print("   ollama pull llama3.2:latest")
        return False
    
    # 3. 测试配置系统
    print("\n3. 测试配置系统...")
    print(f"   当前模式: {model_switcher.get_current_mode()}")
    print(f"   使用本地模型: {config.is_using_local()}")
    
    # 4. 测试模型获取
    print("\n4. 测试各 Agent 模型配置...")
    agents = ['question_analyzer', 'web_searcher', 'analysis_chain', 'report_generator']
    
    for agent in agents:
        model = config.get_model(agent)
        print(f"   {agent}: {model}")
    
    # 5. 测试模型切换
    print("\n5. 测试模型切换...")
    
    original_mode = config.is_using_local()
    
    # 切换到本地模式
    success = await model_switcher.switch_to_local()
    if success:
        print("   ✅ 成功切换到本地模式")
        print(f"   当前模式: {model_switcher.get_current_mode()}")
    else:
        print("   ❌ 切换到本地模式失败")
    
    # 切换回云端模式
    await model_switcher.switch_to_cloud()
    print("   ✅ 成功切换到云端模式")
    print(f"   当前模式: {model_switcher.get_current_mode()}")
    
    # 恢复原始模式
    if original_mode:
        await model_switcher.switch_to_local()
    
    print("\n✅ Ollama 集成测试完成！")
    return True

async def test_simple_agent():
    """测试简单的 Agent 调用"""
    print("\n=== 简单 Agent 测试 ===\n")
    
    try:
        from research_agent.question_analyzer import analyze_question
        
        print("正在测试问题分析 Agent...")
        
        # 强制使用本地模型进行测试
        os.environ["USE_LOCAL_MODEL"] = "true"
        
        test_question = "什么是人工智能？"
        print(f"测试问题: {test_question}")
        
        result = await analyze_question(test_question)
        print(f"分析结果: {result[:200]}..." if len(result) > 200 else result)
        
        print("✅ Agent 测试成功！")
        
    except Exception as e:
        print(f"❌ Agent 测试失败: {e}")
        return False
    
    return True

async def main():
    """主测试函数"""
    print("Ollama 集成测试工具")
    print("请确保已安装 Ollama 并下载了模型\n")
    
    # 基础集成测试
    integration_ok = await test_ollama_integration()
    
    if not integration_ok:
        print("\n⚠️  基础集成测试未通过，跳过 Agent 测试")
        return
    
    # 询问是否进行 Agent 测试
    print("\n" + "="*50)
    response = input("是否进行 Agent 功能测试? (y/n): ").lower()
    
    if response == 'y':
        await test_simple_agent()
    else:
        print("跳过 Agent 测试")
    
    print("\n测试完成！")

if __name__ == "__main__":
    asyncio.run(main())