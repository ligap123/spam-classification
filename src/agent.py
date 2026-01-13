import os
import re
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class PredictionResult(BaseModel):
    is_spam: bool = Field(description="是否为垃圾短信")
    probability: float = Field(description="垃圾短信的概率")
    model_used: str = Field(description="使用的模型")


class AnalysisResult(BaseModel):
    summary: str = Field(description="短信内容摘要")
    risk_factors: List[str] = Field(description="风险因素列表")
    explanation: str = Field(description="模型预测的解释")
    action_suggestion: str = Field(description="行动建议")


class SpamAgent:
    def __init__(self, ml_model):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        )
        self.ml_model = ml_model

    def _is_chinese(self, text: str) -> bool:
        """检测文本是否包含中文字符"""
        return bool(re.search(r'[\u4e00-\u9fff]', text))

    def _translate_to_english(self, text: str) -> str:
        """将中文文本翻译成英文"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的翻译助手。请将中文短信翻译成英文，保持原意不变，不要添加任何额外内容。"},
                    {"role": "user", "content": f"请将以下中文短信翻译成英文：\n\n{text}"}
                ],
                temperature=0.1,
                max_tokens=500
            )
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            print(f"翻译失败: {e}")
            return text

    def predict_spam(self, text: str, model_name: str = "lightgbm") -> PredictionResult:
        # 如果是中文，先翻译成英文
        if self._is_chinese(text):
            print("检测到中文文本，正在翻译成英文...")
            text = self._translate_to_english(text)
            print(f"翻译结果: {text}")
        
        prediction, probability = self.ml_model.predict(model_name, text)
        return PredictionResult(
            is_spam=bool(prediction),
            probability=float(probability),
            model_used=model_name
        )

    def analyze_with_llm(self, text: str, prediction_result: PredictionResult) -> AnalysisResult:
        prompt = f"""你是一个专业的垃圾短信分析专家。请分析以下短信内容，并提供详细的分析报告。

短信内容: {text}

预测结果:
- 是否为垃圾短信: {prediction_result.is_spam}
- 垃圾短信概率: {prediction_result.probability:.2%}
- 使用的模型: {prediction_result.model_used}

请提供以下分析:
1. 简要摘要短信内容（不超过50字）
2. 识别出导致预测结果的关键风险因素（如：中奖信息、紧急通知、诱导点击等）
3. 解释为什么模型会做出这样的预测
4. 根据预测结果，给出具体的行动建议（如：删除、举报、忽略等）

请用中文回答，保持专业和客观。"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的垃圾短信分析专家，擅长识别和分析垃圾短信的特征。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content

        analysis = self._parse_llm_response(content)
        return analysis

    def _parse_llm_response(self, content: str) -> AnalysisResult:
        summary = ""
        risk_factors = []
        explanation = ""
        action_suggestion = ""

        lines = content.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if "摘要" in line or "summary" in line.lower():
                current_section = "summary"
                continue
            elif "风险因素" in line or "risk" in line.lower():
                current_section = "risk"
                continue
            elif "解释" in line or "explain" in line.lower():
                current_section = "explanation"
                continue
            elif "建议" in line or "action" in line.lower():
                current_section = "action"
                continue
            
            if current_section == "summary":
                summary += line + " "
            elif current_section == "risk":
                if line.startswith("-") or line.startswith("•"):
                    risk_factors.append(line.lstrip("-• ").strip())
            elif current_section == "explanation":
                explanation += line + " "
            elif current_section == "action":
                action_suggestion += line + " "

        return AnalysisResult(
            summary=summary.strip(),
            risk_factors=risk_factors if risk_factors else ["未识别到明显风险因素"],
            explanation=explanation.strip(),
            action_suggestion=action_suggestion.strip()
        )

    def full_analysis(self, text: str, model_name: str = "lightgbm") -> Dict[str, Any]:
        prediction_result = self.predict_spam(text, model_name)
        analysis_result = self.analyze_with_llm(text, prediction_result)
        
        return {
            "prediction": prediction_result.model_dump(),
            "analysis": analysis_result.model_dump()
        }

    def get_model_comparison(self, text: str) -> Dict[str, Any]:
        logreg_pred = self.predict_spam(text, "logreg")
        lgb_pred = self.predict_spam(text, "lightgbm")
        
        return {
            "logistic_regression": logreg_pred.model_dump(),
            "lightgbm": lgb_pred.model_dump(),
            "agreement": logreg_pred.is_spam == lgb_pred.is_spam
        }
