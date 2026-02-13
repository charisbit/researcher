import fast
from typing import Dict, Any
from .config import config


@fast.agent(
    instruction="""你是一个深度分析专家。你的任务是：
1. 对收集到的信息进行多层次分析
2. 识别不同观点和证据
3. 评估信息的质量和一致性
4. 发现知识空白和需要进一步研究的领域

请提供：
- 主要发现总结
- 不同观点对比
- 证据强度评估
- 需要深入研究的问题""",
    model=config.get_model("analysis_chain"),
)
async def analyze_information(search_data: Dict[str, Any], question_analysis: str):
    async with fast.run() as agent:
        analysis_prompt = f"""
基于以下研究问题分析：
{question_analysis}

和搜索数据：
{search_data}

请进行深度分析，重点关注：
1. 关键发现和趋势
2. 不同来源的观点对比
3. 证据的可靠性
4. 存在的争议或不确定性
5. 需要进一步研究的领域
"""
        response = await agent.run(analysis_prompt)
        return response


@fast.agent(
    instruction="""你是一个批判性思维专家。你的任务是：
1. 识别分析中的逻辑漏洞
2. 检查偏见和假设
3. 评估结论的可靠性
4. 提出改进建议""",
    model=config.get_model("analysis_chain"),
)
async def critical_review(analysis: str):
    async with fast.run() as agent:
        review_prompt = f"""
请对以下分析进行批判性审查：
{analysis}

重点检查：
1. 逻辑一致性
2. 潜在偏见
3. 证据充分性
4. 结论的合理性
5. 改进建议
"""
        response = await agent.run(review_prompt)
        return response
