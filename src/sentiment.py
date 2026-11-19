"""VADER sentiment scoring and labels for short social media captions."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def compound_score(text: object) -> float:
    """Return VADER's compound score, treating missing values as neutral text."""
    value = text if isinstance(text, str) else ""
    return float(_analyzer.polarity_scores(value)["compound"])


def label(text: object) -> str:
    """Classify text using VADER's standard compound-score thresholds."""
    score = compound_score(text)
    return "positive" if score >= 0.05 else "negative" if score <= -0.05 else "neutral"
