# 🛡️ 智能垃圾短信分类系统

基于机器学习和 LLM Agent 的智能垃圾短信识别与分析系统，支持中英文短信检测，提供可视化Web界面和命令行工具。

## 📋 项目概述

本项目实现了一个完整的垃圾短信分类系统，集成了传统机器学习与大语言模型技术，具备以下核心特点：

- **多语言支持**: 自动识别并翻译中文短信，实现中英文统一检测
- **双模型架构**: 结合 Logistic Regression（基线）和 LightGBM（高性能）模型
- **LLM 智能分析**: 使用 DeepSeek API 生成详细的风险分析报告
- **可视化界面**: 现代化的 Streamlit Web 界面，提供直观的交互体验
- **完整工作流**: 从数据处理、模型训练到部署应用的全流程实现

## 🚀 技术栈

| 类别 | 技术 | 版本要求 |
|------|------|----------|
| **基础语言** | Python | >= 3.12 |
| **项目管理** | uv | 最新版 |
| **数据处理** | Polars + Pandera | 最新版 |
| **机器学习** | Scikit-learn + LightGBM | 最新版 |
| **LLM 集成** | DeepSeek API | 最新版 |
| **可视化** | Streamlit + Plotly | 最新版 |
| **开发工具** | pytest + ruff + black | 最新版 |

## 📁 项目结构

```
.
├── pyproject.toml          # 项目配置和依赖管理
├── .env                    # 环境变量（API Key）
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
├── README.md               # 项目说明文档
├── styles.css              # 网页样式文件
├── src/                    # 源代码目录
│   ├── __init__.py         # 包初始化
│   ├── data_processing.py  # 数据处理模块
│   ├── models.py           # 机器学习模型
│   ├── agent.py            # LLM Agent 模块
│   ├── train.py            # 模型训练脚本
│   ├── streamlit_app.py    # Streamlit 可视化界面
│   ├── agent_app.py        # 命令行应用
│   └── components.py       # UI 组件模块
├── models/                 # 训练好的模型文件
├── archive/                # 原始数据集
│   └── spam.csv            # SMS Spam Collection Dataset
├── data/                   # 处理后的数据
│   ├── processed_spam.csv  # 预处理后的训练数据
│   └── evaluation_report.json # 模型评估报告
└── test_examples.txt       # 测试示例文本
```

## 📦 快速开始

### 1. 环境准备

确保已安装 Python 3.12+ 和 uv：

```bash
# 安装 uv
pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 配置 PyPI 镜像（可选，加速下载）
uv config set index-url https://mirrors.aliyun.com/pypi/simple/
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置 API Key

复制并配置环境变量文件：

```bash
cp .env.example .env
```

在 `.env` 文件中填入 DeepSeek API Key：

```bash
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. 训练模型

```bash
uv run python -m src.train
```

训练完成后，模型将保存在 `models/` 目录中，评估报告保存在 `data/evaluation_report.json` 中。

### 5. 运行应用

#### 方式 A: Streamlit Web 界面（推荐）

```bash
uv run streamlit run src/streamlit_app.py
```

访问地址：http://localhost:8501

#### 方式 B: 命令行工具

```bash
# 单条短信分析
uv run python -m src.agent_app --text "恭喜您获得iPhone 15 Pro Max，点击链接领取：http://fake-link.com"

# 模型对比分析
uv run python -m src.agent_app --text "中奖通知" --compare

# 交互式模式
uv run python -m src.agent_app --interactive
```

## 🎯 功能特性

### 1. 数据处理模块 (`data_processing.py`)

- ✅ 数据加载与验证（使用 Pandera Schema）
- ✅ 文本清洗（去除 URL、数字、标点等）
- ✅ 批量文本处理（高效处理大规模数据）
- ✅ 训练集/测试集智能划分
- ✅ 数据质量检查与报告

### 2. 机器学习模块 (`models.py`)

- ✅ `SpamClassifier` 类封装完整流程
- ✅ **Logistic Regression**: 基线模型，可解释性强
- ✅ **LightGBM**: 高性能模型，精度高速度快
- ✅ TF-IDF 特征提取
- ✅ 模型评估、保存和加载
- ✅ 支持实时预测

### 3. LLM Agent 模块 (`agent.py`)

- ✅ **智能语言检测**: 自动识别中英文短信
- ✅ **自动翻译功能**: 调用 DeepSeek API 将中文翻译成英文
- ✅ **垃圾短信预测**: 集成机器学习模型
- ✅ **LLM 分析报告**: 生成详细的风险因素分析
- ✅ **模型对比**: 支持两个模型结果对比
- ✅ **行动建议**: 提供具体的应对措施

### 4. 可视化界面 (`streamlit_app.py`)

- ✅ 现代化深色主题设计
- ✅ 直观的短信输入界面
- ✅ 实时分析结果展示
- ✅ 模型对比功能
- ✅ 性能指标可视化
- ✅ 示例短信测试
- ✅ 响应式布局设计

## 📊 模型性能

训练后的模型性能指标如下（基于测试集）：

### Logistic Regression
- **准确率 (Accuracy)**: 97.93%
- **F1 分数**: 92.20%
- **Macro F1**: 95.51%
- **ROC-AUC**: 99.51%

### LightGBM
- **准确率 (Accuracy)**: 97.75%
- **F1 分数**: 91.23%
- **Macro F1**: 94.97%
- **ROC-AUC**: 98.70%

所有指标均远超目标要求：
- ✅ Accuracy ≥ 0.85 (达成)
- ✅ Macro-F1 ≥ 0.80 (达成)
- ✅ ROC-AUC ≥ 0.90 (达成)

详细的混淆矩阵和分类报告可在 Web 界面中查看。

## 🎨 界面预览

### Web 界面主要功能

1. **短信分析区域**: 输入短信内容，选择模型，支持模型对比
2. **分析结果展示**: 显示预测结果、内容摘要、风险因素
3. **模型性能指标**: 展示混淆矩阵和分类报告
4. **示例短信库**: 提供多种类型的示例短信
5. **系统信息**: 技术栈和课程要求说明

## 📝 使用示例

### 中文垃圾短信检测
```bash
输入: 恭喜您获得iPhone 15 Pro Max，点击链接领取：http://fake-link.com
翻译: Congratulations on winning an iPhone 15 Pro Max...
预测: 🚨 垃圾短信 (89.98%)
```

### 中文正常短信检测
```bash
输入: 明天下午3点开会，请准时参加
翻译: Meeting at 3 PM tomorrow, please be on time.
预测: ✅ 正常短信 (0.17%)
```

## ⚠️ 注意事项

- **API Key 安全**: 不要将 `.env` 文件提交到 Git 仓库
- **模型文件**: 训练好的模型保存在 `models/` 目录中
- **数据文件**: 处理后的数据保存在 `data/` 目录中
- **Python 版本**: 确保使用 Python 3.12+ 版本
- **网络连接**: 运行时需要网络连接以调用 LLM API

## 📚 课程要求对照

### Level 2 必做部分
- ✅ **数据处理**: 文本清洗策略说明，使用 Pandera 定义 Schema
- ✅ **机器学习**: TF-IDF + LogReg 基线，达到 Accuracy ≥ 0.85 或 Macro-F1 ≥ 0.80
- ✅ **Agent**: 实现「预测 → 归因 → 处置建议」闭环，至少 2 个 tool

### 高级功能扩展
- ✅ **多语言支持**: 实现中英文短信统一检测
- ✅ **可视化界面**: 提供现代化的 Web 应用
- ✅ **模型对比**: 支持多个模型结果对比
- ✅ **LLM 增强**: 集成大语言模型进行智能分析

## 📄 许可证

本项目为课程作业，仅供学习使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请联系项目维护者。

---

**更新时间**: 2026-01-13
**版本**: v1.0.0