import json
from pathlib import Path

import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt

from src.data_processing import load_data, validate_data, preprocess_data, save_processed_data, prepare_train_test_split
from src.models import SpamClassifier

sns.set_theme(style="whitegrid")


def main():
    print("=" * 50)
    print("垃圾短信分类模型训练")
    print("=" * 50)

    print("\n1. 加载数据...")
    df = load_data()
    print(f"   数据集大小: {len(df)} 条")
    print(f"   标签分布:\n{df['label'].value_counts()}")

    print("\n2. 验证数据...")
    df = validate_data(df)
    print("   数据验证通过")

    print("\n3. 预处理数据...")
    df = preprocess_data(df)
    print(f"   预处理后数据集大小: {len(df)} 条")

    print("\n4. 保存处理后的数据...")
    save_processed_data(df)
    print("   数据已保存到 data/processed_spam.parquet")

    print("\n5. 划分训练集和测试集...")
    train_df, test_df = prepare_train_test_split(df)
    print(f"   训练集大小: {len(train_df)} 条")
    print(f"   测试集大小: {len(test_df)} 条")

    print("\n6. 训练模型...")
    classifier = SpamClassifier()

    print("   训练 Logistic Regression 基线模型...")
    classifier.train_logistic_regression(train_df)

    print("   训练 LightGBM 模型...")
    classifier.train_lightgbm(train_df)

    print("\n7. 评估模型...")
    logreg_metrics = classifier.evaluate("logreg", test_df)
    lgb_metrics = classifier.evaluate("lightgbm", test_df)

    print("\n   Logistic Regression 性能:")
    print(f"   - Accuracy: {logreg_metrics['accuracy']:.4f}")
    print(f"   - F1 Score: {logreg_metrics['f1_score']:.4f}")
    print(f"   - Macro F1: {logreg_metrics['macro_f1']:.4f}")
    print(f"   - ROC-AUC: {logreg_metrics['roc_auc']:.4f}")

    print("\n   LightGBM 性能:")
    print(f"   - Accuracy: {lgb_metrics['accuracy']:.4f}")
    print(f"   - F1 Score: {lgb_metrics['f1_score']:.4f}")
    print(f"   - Macro F1: {lgb_metrics['macro_f1']:.4f}")
    print(f"   - ROC-AUC: {lgb_metrics['roc_auc']:.4f}")

    print("\n8. 保存模型...")
    classifier.save_models()
    print("   模型已保存到 models/ 目录")

    print("\n9. 生成评估报告...")
    save_evaluation_report(logreg_metrics, lgb_metrics)

    print("\n" + "=" * 50)
    print("训练完成！")
    print("=" * 50)


def save_evaluation_report(logreg_metrics, lgb_metrics):
    report = {
        "logistic_regression": {
            "accuracy": logreg_metrics["accuracy"],
            "f1_score": logreg_metrics["f1_score"],
            "macro_f1": logreg_metrics["macro_f1"],
            "roc_auc": logreg_metrics["roc_auc"],
            "confusion_matrix": logreg_metrics["confusion_matrix"]
        },
        "lightgbm": {
            "accuracy": lgb_metrics["accuracy"],
            "f1_score": lgb_metrics["f1_score"],
            "macro_f1": lgb_metrics["macro_f1"],
            "roc_auc": lgb_metrics["roc_auc"],
            "confusion_matrix": lgb_metrics["confusion_matrix"]
        }
    }

    report_path = Path(__file__).parent.parent / "data" / "evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"   评估报告已保存到 {report_path}")


if __name__ == "__main__":
    main()
