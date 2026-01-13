import re
import string
import os
from pathlib import Path
from typing import List

import nltk
import polars as pl
import pandera as pa
from pandera.typing import DataFrame, Series
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

ARCHIVE_DIR = Path(__file__).parent.parent / "archive"


class SpamSchema(pa.DataFrameModel):
    label: Series[str] = pa.Field(isin=["ham", "spam"])
    text: Series[str] = pa.Field(nullable=False)


def download_nltk_data():
    try:
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
    except Exception as e:
        print(f"   警告: NLTK 数据下载失败 ({e})，将跳过 NLTK 功能")


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[0-9]+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_text_batch(texts: List[str]) -> List[str]:
    return [clean_text(text) for text in texts]


def load_data() -> pl.DataFrame:
    df = pl.read_csv(ARCHIVE_DIR / "spam.csv", encoding="utf-8-lossy")
    df = df.rename({"v1": "label", "v2": "text"})
    return df


def validate_data(df: pl.DataFrame) -> pl.DataFrame:
    pandas_df = df.to_pandas()
    SpamSchema.validate(pandas_df)
    return df


def preprocess_data(df: pl.DataFrame, batch_size: int = 1000) -> pl.DataFrame:
    download_nltk_data()
    
    texts = df["text"].to_list()
    total = len(texts)
    
    cleaned_texts = []
    
    print("   开始预处理文本...")
    for i in tqdm(range(0, total, batch_size), desc="   预处理进度"):
        batch = texts[i:i + batch_size]
        cleaned_batch = clean_text_batch(batch)
        cleaned_texts.extend(cleaned_batch)
    
    df = df.with_columns(
        pl.Series("cleaned_text", cleaned_texts)
    )
    df = df.filter(pl.col("cleaned_text").str.len_chars() > 0)
    
    print(f"   预处理完成，剩余 {len(df)} 条数据")
    return df


def save_processed_data(df: pl.DataFrame, filename: str = "processed_spam.csv"):
    output_path = DATA_DIR / filename
    original_cwd = os.getcwd()
    try:
        os.chdir(DATA_DIR)
        df.write_csv(filename)
    finally:
        os.chdir(original_cwd)
    return output_path


def load_processed_data(filename: str = "processed_spam.csv") -> pl.DataFrame:
    output_path = DATA_DIR / filename
    original_cwd = os.getcwd()
    try:
        os.chdir(DATA_DIR)
        return pl.read_csv(filename, encoding="utf-8-lossy")
    finally:
        os.chdir(original_cwd)


def prepare_train_test_split(df: pl.DataFrame, test_size: float = 0.2, random_state: int = 42):
    df = df.with_columns(
        pl.col("label").map_elements(lambda x: 1 if x == "spam" else 0, return_dtype=pl.Int32).alias("label_encoded")
    )
    df_shuffled = df.sample(fraction=1.0, seed=random_state)
    n_test = int(len(df_shuffled) * test_size)
    
    train_df = df_shuffled.slice(0, len(df_shuffled) - n_test)
    test_df = df_shuffled.slice(len(df_shuffled) - n_test, n_test)
    
    return train_df, test_df
