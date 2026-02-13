import fast
from .config import config

@fast.agent(
    instruction="""你是一个研究问题分析专家。你的任务是：
1. 分析用户提出的研究问题
2. 识别问题的关键领域和概念
3. 将复杂问题分解为可研究的子问题
4. 生成搜索关键词和查询策略

请以结构化的方式输出：
- 问题分类
- 关键概念
- 子问题列表
- 搜索关键词"""
    model=config.get_model("question_analyzer")
)
async def analyze_question(question: str):
    async with fast.run() as agent:
        response = await agent.run(f"请分析以下研究问题：{question}")
        return response