# AI 研究助手

基于 [fast-agent](https://github.com/evalstate/fast-agent) 构建的智能研究原型系统，能够自动执行研究任务并生成带引用的报告。

## 功能特性

1. **智能问题分析** - 自动分解复杂研究问题
2. **自动资料检索** - 使用 Web 搜索收集相关信息
3. **多阶段分析** - 深度分析和批判性审查
4. **报告生成** - 生成结构化的学术报告
5. **引用管理** - 自动格式化引用和参考文献
6. **🆕 本地模型支持** - 集成 Ollama，支持本地私密运行

## 系统架构

```
用户输入问题 → 问题分析 → 资料检索 → 多阶段分析 → 报告生成
     ↓            ↓          ↓           ↓           ↓
  研究问题    关键词提取   搜索结果   深度分析   带引用报告
```

## 安装和配置

### 1. 环境要求
- Python 3.8+
- fast-agent-mcp

### 2. 安装依赖
```bash
pip install -e .
```

### 3. 配置模型

#### 选项 A: 使用云端模型
复制 `.env.example` 为 `.env` 并填入您的 API 密钥：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
USE_LOCAL_MODEL=false
```

#### 选项 B: 使用本地 Ollama 模型 (推荐)
1. 安装并配置 Ollama，详见 [Ollama 集成指南](OLLAMA_SETUP.md)
2. 编辑 `.env` 文件：
```
USE_LOCAL_MODEL=true
OLLAMA_BASE_URL=http://localhost:11434/v1
```

#### 混合模式
可以同时配置云端和本地模型，在 `config.yaml` 中指定不同任务使用不同模型。

## 使用方法

### 交互式运行
```bash
python run_research.py
```

### 程序化使用
```python
from research_agent.main import research_workflow

result = await research_workflow("什么是人工智能的未来发展趋势？")
print(result['final_report'])
```

## 示例用法

```
=== AI 研究助手 ===
基于 fast-agent 构建的智能研究系统

请输入您的研究问题: 量子计算的发展现状和挑战

==================================================
开始研究问题: 量子计算的发展现状和挑战
步骤 1: 分析研究问题...
步骤 2: 执行网络搜索...
步骤 3: 进行深度分析...
步骤 4: 批判性审查...
步骤 5: 生成研究报告...
步骤 6: 格式化引用...
==================================================

研究完成！报告已保存为: research_report_20241201_143022.md
```

## 核心组件

### 1. 问题分析器 (question_analyzer.py)
- 分析研究问题的关键概念
- 分解复杂问题为子问题
- 生成搜索策略

### 2. Web 搜索器 (web_searcher.py)
- 执行关键词搜索
- 评估结果相关性
- 提取关键信息

### 3. 分析链 (analysis_chain.py)
- 深度信息分析
- 批判性思维审查
- 多层次理解

### 4. 报告生成器 (report_generator.py)
- 结构化报告撰写
- 学术引用格式化
- 文件保存管理

## 扩展功能

### 集成更多数据源
- 学术数据库 API
- 新闻 API
- 社交媒体数据

### 增强分析能力
- 多语言支持
- 图表生成
- 数据可视化

### 优化工作流
- 并行处理
- 缓存机制
- 结果验证

## 技术栈

- **fast-agent**: Agent 框架和工作流管理
- **MCP**: 模型上下文协议用于工具集成
- **Anthropic Claude**: 主要语言模型
- **aiohttp**: 异步 HTTP 请求
- **asyncio**: 异步编程支持

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

如有问题，请查看：
1. [fast-agent 文档](https://fast-agent.ai/)
2. [MCP 文档](https://modelcontextprotocol.io/)
3. 项目 Issues