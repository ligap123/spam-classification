import joblib
from pathlib import Path
from typing import Tuple, Dict, Any

import lightgbm as lgb
import numpy as np
import polars as pl
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.pipeline import Pipeline

MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)


class SpamClassifier:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.models = {}
        self.metrics = {}

    def train_logistic_regression(self, train_df: pl.DataFrame) -> Pipeline:
        X_train = train_df["cleaned_text"].to_list()
        y_train = train_df["label_encoded"].to_list()
        
        pipeline = Pipeline([
            ("tfidf", self.tfidf),
            ("clf", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"))
        ])
        
        pipeline.fit(X_train, y_train)
        self.models["logreg"] = pipeline
        return pipeline

    def train_lightgbm(self, train_df: pl.DataFrame) -> lgb.LGBMClassifier:
        X_train = self.tfidf.fit_transform(train_df["cleaned_text"].to_list())
        y_train = train_df["label_encoded"].to_list()
        
        model = lgb.LGBMClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=-1,
            random_state=42,
            class_weight="balanced",
            verbose=-1
        )
        
        model.fit(X_train, y_train)
        self.models["lightgbm"] = model
        return model

    def evaluate(self, model_name: str, test_df: pl.DataFrame) -> Dict[str, Any]:
        model = self.models[model_name]
        X_test = test_df["cleaned_text"].to_list()
        y_test = test_df["label_encoded"].to_list()
        
        if model_name == "logreg":
            X_test_tfidf = model.named_steps["tfidf"].transform(X_test)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            X_test_tfidf = self.tfidf.transform(X_test)
            y_pred = model.predict(X_test_tfidf)
            y_proba = model.predict_proba(X_test_tfidf)[:, 1]
        
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "macro_f1": f1_score(y_test, y_pred, average="macro"),
            "roc_auc": roc_auc_score(y_test, y_proba),
            "classification_report": classification_report(y_test, y_pred, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
        }
        
        self.metrics[model_name] = metrics
        return metrics

    def predict(self, model_name: str, text: str) -> Tuple[int, float]:
        model = self.models[model_name]
        
        if model_name == "logreg":
            from src.data_processing import clean_text
            cleaned_text = clean_text(text)
            prediction = model.predict([cleaned_text])[0]
            probability = model.predict_proba([cleaned_text])[0, 1]
        else:
            from src.data_processing import clean_text
            cleaned_text = clean_text(text)
            text_tfidf = self.tfidf.transform([cleaned_text])
            prediction = model.predict(text_tfidf)[0]
            probability = model.predict_proba(text_tfidf)[0, 1]
        
        return prediction, probability

    def save_models(self):
        joblib.dump(self.models["logreg"], MODEL_DIR / "logreg_model.joblib")
        joblib.dump(self.models["lightgbm"], MODEL_DIR / "lightgbm_model.joblib")
        joblib.dump(self.tfidf, MODEL_DIR / "tfidf_vectorizer.joblib")
        joblib.dump(self.metrics, MODEL_DIR / "metrics.joblib")

    def load_models(self):
        self.models["logreg"] = joblib.load(MODEL_DIR / "logreg_model.joblib")
        self.models["lightgbm"] = joblib.load(MODEL_DIR / "lightgbm_model.joblib")
        self.tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer.joblib")
        self.metrics = joblib.load(MODEL_DIR / "metrics.joblib")
