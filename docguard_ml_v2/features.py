from __future__ import annotations

from typing import Any

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline

from docguard_ml_v2.data_contract import serialize_model_row


class SafeTextTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X: list[dict[str, Any]], y: list[Any] | None = None) -> "SafeTextTransformer":
        return self

    def transform(self, X: list[dict[str, Any]]) -> list[str]:
        return [serialize_model_row(row) for row in X]


def word_tfidf(*, min_df: int = 1, max_features: int = 60000) -> Pipeline:
    return Pipeline(
        [
            ("text", SafeTextTransformer()),
            ("tfidf", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=min_df, max_features=max_features, sublinear_tf=True, token_pattern=r"(?u)\b[\w./:@+\-#]+\b")),
        ]
    )


def char_tfidf(*, min_df: int = 1, max_features: int = 80000) -> Pipeline:
    return Pipeline(
        [
            ("text", SafeTextTransformer()),
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=min_df, max_features=max_features, sublinear_tf=True)),
        ]
    )


def word_char_tfidf(*, min_df: int = 1) -> FeatureUnion:
    return FeatureUnion([("word", word_tfidf(min_df=min_df)), ("char", char_tfidf(min_df=min_df))])

