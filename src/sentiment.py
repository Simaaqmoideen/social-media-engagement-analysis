"""Optional: VADER sentiment for captions/comments."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_an = SentimentIntensityAnalyzer()


def label(text: str) -> str:
    s = _an.polarity_scores(text)["compound"]
    return "positive" if s >= 0.05 else "negative" if s <= -0.05 else "neutral"
