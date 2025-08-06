import fast
from typing import Dict, Any, List
from datetime import datetime
from .config import config

@fast.agent(
    instruction="""你是一个专业的研究报告撰写专家。你的任务是：
1. 将分析结果整合为结构化报告
2. 确保引用格式正确和完整
3. 提供清晰的摘要和结论
4. 保持学术写作标准

报告应包含：
- 执行摘要
- 研究问题和方法
- 主要发现
- 详细分析
- 结论和建议
- 参考文献

使用清晰的标题层次和专业的学术语言。""",
    model=config.get_model("report_generator")
)
async def generate_report(
    original_question: str,
    question_analysis: str,
    search_results: Dict[str, Any],
    analysis: str,
    critical_review: str
):
    async with fast.run() as agent:
        report_prompt = f"""
请基于以下信息生成一份完整的研究报告：

原始研究问题：
{original_question}

问题分析：
{question_analysis}

搜索结果：
{search_results}

深度分析：
{analysis}

批判性审查：
{critical_review}

请生成一份结构化的研究报告，包含适当的引用和学术格式。
"""
        response = await agent.run(report_prompt)
        return response

@fast.agent(
    instruction="""你是一个引用格式专家。你的任务是：
1. 从文本中提取所有引用来源
2. 标准化引用格式
3. 生成完整的参考文献列表
4. 确保引用的准确性和一致性""",
    model=config.get_model("report_generator")
)
async def format_citations(report_text: str, sources: List[Dict]):
    async with fast.run() as agent:
        citation_prompt = f"""
请为以下报告添加规范的引用格式：

报告内容：
{report_text}

可用来源：
{sources}

请使用 APA 格式进行引用，并在报告末尾生成完整的参考文献列表。
"""
        response = await agent.run(citation_prompt)
        return response

def save_report(report_content: str, filename: str = None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return filename