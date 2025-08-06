# Ollama 集成指南

本文档说明如何在 AI 研究助手中配置和使用 Ollama 本地模型。

## 什么是 Ollama？

Ollama 是一个轻量级、可扩展的框架，用于在本地运行大型语言模型。使用 Ollama 的优势：

- **隐私保护**: 数据不离开本地环境
- **成本控制**: 无需付费 API 调用
- **离线工作**: 无需互联网连接
- **定制化**: 可以使用专门的模型

## 安装 Ollama

### macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
下载并安装 [Ollama for Windows](https://ollama.ai/download/windows)

## 配置推荐模型

### 1. 下载推荐模型

```bash
# 通用模型 (推荐)
ollama pull llama3.2:latest

# 中文优化模型
ollama pull qwen2.5:latest

# 代码生成模型
ollama pull codellama:latest

# 轻量级模型 (较快)
ollama pull mistral:latest
```

### 2. 验证安装

```bash
# 列出已安装的模型
ollama list

# 测试模型
ollama run llama3.2:latest
```

## 配置研究助手

### 1. 环境变量配置

复制并编辑环境变量文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```bash
# 启用本地模型
USE_LOCAL_MODEL=true

# Ollama 配置 (通常无需修改)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama
```

### 2. 配置文件定制

编辑 `config.yaml` 来指定使用的模型：

```yaml
defaults:
  use_local: true  # 使用本地模型
  local_model: "generic.llama3.2:latest"

# 为不同功能指定不同模型
agents:
  question_analyzer:
    local: "generic.llama3.2:latest"  # 问题分析
  
  web_searcher:
    local: "generic.qwen2.5:latest"   # 搜索分析 (中文优化)
  
  analysis_chain:
    local: "generic.llama3.2:latest"  # 深度分析
  
  report_generator:
    local: "generic.llama3.2:latest"  # 报告生成
```

## 模型选择建议

### 按性能分类

**高性能 (需要更多资源)**
- `llama3.2:latest` - 通用能力强，适合复杂分析
- `qwen2.5:latest` - 中文优化，适合中文研究

**中等性能 (平衡选择)**
- `mistral:latest` - 速度较快，质量不错

**轻量级 (快速响应)**
- `llama3.2:1b` - 最小模型，适合简单任务

### 按用途分类

**研究分析**: `llama3.2:latest`
**中文处理**: `qwen2.5:latest`  
**代码相关**: `codellama:latest`
**快速原型**: `mistral:latest`

## 使用方法

### 1. 启动 Ollama 服务

```bash
# 启动服务 (后台运行)
ollama serve

# 或者 (前台运行，可看到日志)
ollama serve --verbose
```

### 2. 运行研究助手

```bash
# 使用本地模型
USE_LOCAL_MODEL=true python run_research.py

# 或者直接运行 (如果已在 .env 中配置)
python run_research.py
```

### 3. 切换模型模式

在程序中动态切换：

```python
from research_agent.model_switcher import model_switcher

# 切换到本地模型
await model_switcher.switch_to_local()

# 切换到云端模型
await model_switcher.switch_to_cloud()

# 检查当前模式
print(f"当前使用: {model_switcher.get_current_mode()}模型")
```

## 性能优化

### 1. 硬件要求

**最低要求**:
- RAM: 8GB (可运行 7B 参数模型)
- 存储: 4GB 可用空间

**推荐配置**:
- RAM: 16GB+ (可运行 13B+ 参数模型)
- GPU: 支持 CUDA 的显卡 (可选，加速推理)

### 2. 模型参数调优

在 `config.yaml` 中添加性能设置：

```yaml
ollama:
  base_url: "http://localhost:11434/v1"
  api_key: "ollama"
  timeout: 120  # 增加超时时间
  
  # 模型参数 (可选)
  temperature: 0.7
  max_tokens: 2048
  top_p: 0.9
```

## 故障排除

### 常见问题

**1. "Ollama 服务未运行"**
```bash
# 检查服务状态
ps aux | grep ollama

# 重启服务
pkill ollama
ollama serve
```

**2. "模型下载失败"**
```bash
# 检查网络连接
ping ollama.ai

# 重新下载模型
ollama pull llama3.2:latest --verbose
```

**3. "内存不足"**
```bash
# 使用较小的模型
ollama pull llama3.2:1b

# 或清理不用的模型
ollama rm <model-name>
```

**4. "响应太慢"**
- 使用较小的模型 (`mistral:latest`)
- 减少 `max_tokens` 设置
- 考虑升级硬件

### 日志检查

```bash
# 查看 Ollama 日志
ollama logs

# 查看研究助手日志
python run_research.py --verbose
```

## 云端 + 本地混合模式

可以配置不同任务使用不同模型：

```yaml
agents:
  question_analyzer:
    cloud: "anthropic.claude-3-sonnet-latest"  # 云端 - 复杂分析
    local: "generic.llama3.2:latest"           # 本地 - 备用
  
  web_searcher:
    cloud: "anthropic.claude-3-haiku-latest"   # 云端 - 快速处理
    local: "generic.mistral:latest"            # 本地 - 轻量级
```

通过环境变量控制：
```bash
# 问题分析用云端，其他用本地
QUESTION_ANALYZER_USE_CLOUD=true python run_research.py
```

## 进阶配置

### 自定义模型

```bash
# 创建自定义模型文件
ollama create my-research-model -f ./Modelfile

# 使用自定义模型
# 在 config.yaml 中设置: "generic.my-research-model:latest"
```

### API 服务器模式

```bash
# 启动 API 服务器
ollama serve --host 0.0.0.0 --port 11434

# 配置远程 Ollama
OLLAMA_BASE_URL=http://remote-server:11434/v1
```

## 总结

Ollama 集成为研究助手提供了本地化、私密化的 AI 能力。根据你的硬件配置和需求选择合适的模型，可以在保护隐私的同时获得优秀的研究体验。