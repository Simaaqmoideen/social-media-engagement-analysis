"""python src/generate_data.py && python src/analysis.py  -> reports/*.png and reports/summary.txt"""
import pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


def bar(series, title, fname, pct=True):
    ax = series.plot(kind="bar", figsize=(7, 3.5), color="#3b6ea5")
    ax.set_title(title); ax.set_ylabel("avg engagement rate"); plt.xticks(rotation=30)
    plt.savefig(REP / fname, dpi=120, bbox_inches="tight"); plt.close()


def main():
    REP.mkdir(exist_ok=True)
    df = load()
    by_type = df.groupby("type")["er"].mean().sort_values(ascending=False)
    by_hour = df.groupby("hour")["er"].mean()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_day = df.groupby("weekday")["er"].mean().reindex(order)
    by_tags = df.groupby("n_tags")["er"].mean()
    tag_rows = df.assign(tag=df.hashtags.apply(extract_hashtags)).explode("tag").dropna(subset=["tag"])
    by_tag = tag_rows.groupby("tag")["er"].agg(["mean", "count"]).sort_values("mean", ascending=False)
    bar(by_type, "Engagement by post type", "by_type.png")
    bar(by_hour, "Engagement by hour of day", "by_hour.png")
    bar(by_day, "Engagement by weekday", "by_weekday.png")
    bar(by_tags, "Engagement by number of hashtags", "by_n_tags.png")
    bar(by_tag["mean"], "Engagement by hashtag", "by_hashtag.png")
    lines = ["TOP FINDINGS (auto-generated; verify before sharing)",
             f"- Best post type: {by_type.index[0]} ({by_type.iloc[0]:.2%} avg ER)",
             f"- Best hour: {by_hour.idxmax()}:00 ({by_hour.max():.2%})",
             f"- Best weekday: {by_day.idxmax()} ({by_day.max():.2%})",
             f"- Top hashtag: {by_tag.index[0]} (n={int(by_tag['count'].iloc[0])})",
             "- NOTE: these are associations, not proof of cause."]
    (REP / "summary.txt").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
