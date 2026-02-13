import fast
from .config import config

@fast.agent(
    instruction="""你是一个信息检索专家。你的任务是：
1. 根据关键词执行网络搜索
2. 评估搜索结果的相关性和可信度
3. 提取关键信息和数据
4. 记录信息来源以供引用

请为每个搜索结果提供：
- 标题
- 来源URL
- 关键信息摘要
- 可信度评估""",
    model=config.get_model("web_searcher")
)
async def search_web(keywords: List[str], max_results: int = 5):
    async with fast.run() as agent:
        search_results = []
        
        for keyword in keywords:
            try:
                # 这里使用一个简化的搜索模拟
                # 在实际实现中，可以集成 Google Search API 或其他搜索服务
                result = {
                    "keyword": keyword,
                    "title": f"搜索结果: {keyword}",
                    "url": f"https://example.com/search?q={keyword}",
                    "summary": f"关于 {keyword} 的相关信息...",
                    "credibility": "中等"
                }
                search_results.append(result)
            except Exception as e:
                print(f"搜索 {keyword} 时出错: {e}")
        
        # 让 agent 分析和整理搜索结果
        analysis_prompt = f"请分析以下搜索结果，提取关键信息：\n{search_results}"
        response = await agent.run(analysis_prompt)
        
        return {
            "raw_results": search_results,
            "analysis": response
        }