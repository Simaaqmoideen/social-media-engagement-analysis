"""python src/generate_data.py && python src/analysis.py  -> reports/*.png and reports/summary.txt"""
import pathlib
import sys
import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.clean import load_posts

ROOT = pathlib.Path(__file__).resolve().parents[1]
REP = ROOT / "reports"


def engagement_rate(likes: int, comments: int, shares: int, followers: int) -> float:
    """(likes + comments + shares) / followers; 0 when followers is 0."""
    return (likes + comments + shares) / followers if followers else 0.0


def extract_hashtags(text: object) -> list[str]:
    if not isinstance(text, str):
        return []
    return sorted({w.lower() for w in text.split() if w.startswith("#") and len(w) > 1})


def load() -> pd.DataFrame:
    """Load cleaned posts and derive basic engagement/time features."""
    df = load_posts()
    df["er"] = [
        engagement_rate(*r)
        for r in zip(df.likes, df.comments, df.shares, df.followers)
    ]
    df["hour"], df["weekday"] = df.timestamp.dt.hour, df.timestamp.dt.day_name()
    df["n_tags"] = df.hashtags.apply(lambda s: len(extract_hashtags(s)))
    return df


def main():
    """Run the chart pack and print the measured descriptive takeaways."""
    from src.charts import create_chart_pack

    REP.mkdir(exist_ok=True)
    df = load()
    takeaways = create_chart_pack(df, REP)
    print(f"Rows analyzed: {len(df):,}; charts created: 6")
    print("\n".join(f"- {takeaway}" for takeaway in takeaways))


if __name__ == "__main__":
    main()
