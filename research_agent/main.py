import fast
from dotenv import load_dotenv

from .question_analyzer import analyze_question
from .web_searcher import search_web
from .analysis_chain import analyze_information, critical_review
from .report_generator import generate_report, format_citations, save_report

load_dotenv()

@fast.chain(
    agents=[
        "analyze_question",
        "search_web", 
        "analyze_information",
        "critical_review",
        "generate_report",
        "format_citations"
    ]
)
async def research_workflow(research_question: str):
    """
    完整的研究工作流程
    """
    print(f"开始研究问题: {research_question}")
    
    # 1. 分析问题
    print("步骤 1: 分析研究问题...")
    question_analysis = await analyze_question(research_question)
    print("问题分析完成")
    
    # 2. 提取搜索关键词并执行搜索
    print("步骤 2: 执行网络搜索...")
    # 简化版：从问题中提取关键词
    keywords = research_question.split()[:3]  # 简单的关键词提取
    search_results = await search_web(keywords)
    print("搜索完成")
    
    # 3. 深度分析
    print("步骤 3: 进行深度分析...")
    analysis = await analyze_information(search_results, question_analysis)
    print("分析完成")
    
    # 4. 批判性审查
    print("步骤 4: 批判性审查...")
    review = await critical_review(analysis)
    print("审查完成")
    
    # 5. 生成报告
    print("步骤 5: 生成研究报告...")
    report = await generate_report(
        research_question,
        question_analysis,
        search_results,
        analysis,
        review
    )
    print("报告生成完成")
    
    # 6. 格式化引用
    print("步骤 6: 格式化引用...")
    sources = search_results.get('raw_results', [])
    final_report = await format_citations(report, sources)
    print("引用格式化完成")
    
    # 7. 保存报告
    filename = save_report(final_report)
    print(f"报告已保存为: {filename}")
    
    return {
        "question": research_question,
        "analysis": question_analysis,
        "search_results": search_results,
        "detailed_analysis": analysis,
        "critical_review": review,
        "final_report": final_report,
        "saved_file": filename
    }

async def main():
    """
    主函数 - 用于交互式研究
    """
    print("=== AI 研究助手 ===")
    print("基于 fast-agent 构建的智能研究系统")
    print()
    
    while True:
        research_question = input("请输入您的研究问题 (输入 'quit' 退出): ")
        
        if research_question.lower() == 'quit':
            print("感谢使用 AI 研究助手！")
            break
        
        if not research_question.strip():
            print("请输入有效的研究问题。")
            continue
        
        try:
            print("\n" + "="*50)
            result = await research_workflow(research_question)
            print("="*50)
            print(f"\n研究完成！报告已保存为: {result['saved_file']}")
            print("\n" + "-"*30)
            print("报告预览:")
            print("-"*30)
            print(result['final_report'][:500] + "..." if len(result['final_report']) > 500 else result['final_report'])
            print("\n")
            
        except Exception as e:
            print(f"处理过程中出现错误: {e}")
            print("请检查您的 API 配置和网络连接。")

if __name__ == "__main__":
    asyncio.run(main())