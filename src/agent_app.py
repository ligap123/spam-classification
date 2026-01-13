import argparse
from src.models import SpamClassifier
from src.agent import SpamAgent


def main():
    parser = argparse.ArgumentParser(description="垃圾短信分类 Agent")
    parser.add_argument("--text", type=str, help="要分析的短信内容")
    parser.add_argument("--model", type=str, default="lightgbm", choices=["logreg", "lightgbm"], help="使用的模型")
    parser.add_argument("--compare", action="store_true", help="对比两个模型的结果")
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    
    args = parser.parse_args()

    print("正在加载模型...")
    classifier = SpamClassifier()
    classifier.load_models()
    agent = SpamAgent(classifier)
    print("✅ 模型加载成功\n")

    if args.interactive:
        interactive_mode(agent)
    elif args.text:
        analyze_text(agent, args.text, args.model, args.compare)
    else:
        print("请提供 --text 参数或使用 --interactive 进入交互模式")
        print("示例: uv run python src/agent_app.py --text '中奖通知'")
        print("示例: uv run python src/agent_app.py --interactive")


def analyze_text(agent, text, model, compare):
    print("=" * 60)
    print("短信内容")
    print("=" * 60)
    print(text)
    print()

    if compare:
        print("=" * 60)
        print("模型对比")
        print("=" * 60)
        comparison = agent.get_model_comparison(text)
        
        logreg = comparison["logistic_regression"]
        lgb = comparison["lightgbm"]
        
        print(f"\nLogistic Regression:")
        print(f"  预测: {'垃圾短信' if logreg['is_spam'] else '正常短信'}")
        print(f"  概率: {logreg['probability']:.2%}")
        
        print(f"\nLightGBM:")
        print(f"  预测: {'垃圾短信' if lgb['is_spam'] else '正常短信'}")
        print(f"  概率: {lgb['probability']:.2%}")
        
        print(f"\n一致性: {'✅ 一致' if comparison['agreement'] else '⚠️ 不一致'}")
        print()
    
    print("=" * 60)
    print("预测结果")
    print("=" * 60)
    prediction = agent.predict_spam(text, model)
    
    if prediction.is_spam:
        print(f"🚨 垃圾短信 (概率: {prediction.probability:.2%})")
    else:
        print(f"✅ 正常短信 (垃圾概率: {prediction.probability:.2%})")
    print(f"使用模型: {prediction.model_used}")
    print()

    print("=" * 60)
    print("LLM 分析报告")
    print("=" * 60)
    analysis = agent.analyze_with_llm(text, prediction)
    
    print(f"\n📋 摘要:")
    print(f"  {analysis.summary}")
    
    print(f"\n⚠️ 风险因素:")
    for factor in analysis.risk_factors:
        print(f"  - {factor}")
    
    print(f"\n💡 解释:")
    print(f"  {analysis.explanation}")
    
    print(f"\n🎯 行动建议:")
    print(f"  {analysis.action_suggestion}")
    print()


def interactive_mode(agent):
    print("=" * 60)
    print("交互式模式")
    print("=" * 60)
    print("输入短信内容进行分析，输入 'quit' 退出\n")
    
    while True:
        try:
            text = input("请输入短信内容: ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            if not text:
                continue
            
            model = input("选择模型 (lightgbm/logreg) [默认: lightgbm]: ").strip()
            if not model:
                model = "lightgbm"
            
            compare = input("是否对比模型? (y/n) [默认: n]: ").strip().lower() == 'y'
            
            print()
            analyze_text(agent, text, model, compare)
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}\n")


if __name__ == "__main__":
    main()
