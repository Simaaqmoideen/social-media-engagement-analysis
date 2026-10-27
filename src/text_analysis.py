"""Summarize hashtag and caption-text patterns against observed engagement."""

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from src.analysis import extract_hashtags


def text_summaries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return hashtag and caption-length summaries with sample sizes."""
    tags = df.assign(tag=df["hashtags"].apply(extract_hashtags)).explode("tag")
    tags = tags.dropna(subset=["tag"])
    hashtag_summary = (
        tags.groupby("tag")["er"].agg(mean_er="mean", post_count="count")
        .sort_values(["post_count", "mean_er"], ascending=[False, False])
    )

    captions = df.assign(word_count=df["caption"].fillna("").str.split().str.len())
    captions["caption_length"] = pd.cut(
        captions["word_count"], bins=[-1, 4, 9, float("inf")],
        labels=["0-4 words", "5-9 words", "10+ words"],
    )
    caption_summary = captions.groupby("caption_length", observed=False)["er"].agg(
        mean_er="mean", post_count="count"
    )
    return hashtag_summary, caption_summary


def _bar(summary: pd.DataFrame, label: str, title: str, output: Path) -> None:
    plotted = summary.sort_values("mean_er", ascending=False)
    names = [f"{key} (n={int(count)})" for key, count in zip(plotted.index, plotted["post_count"])]
    fig, axis = plt.subplots(figsize=(9, 4.5))
    bars = axis.bar(names, plotted["mean_er"], color="#3569a8")
    axis.set(title=title, ylabel="Mean engagement rate", xlabel=label)
    axis.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axis.bar_label(bars, labels=[f"{value:.1%}" for value in plotted["mean_er"]], padding=3)
    axis.grid(axis="y", alpha=0.2)
    axis.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def analyze_text(df: pd.DataFrame, output_dir: Path) -> list[str]:
    """Write text summaries and figures; return measured observations."""
    output_dir.mkdir(parents=True, exist_ok=True)
    hashtag_summary, caption_summary = text_summaries(df)
    hashtag_summary.to_csv(output_dir / "hashtag_text_summary.csv")
    caption_summary.to_csv(output_dir / "caption_length_summary.csv")
    _bar(hashtag_summary.head(10), "Hashtag", "Mean engagement for 10 most-used hashtags", output_dir / "hashtag_text.png")
    _bar(caption_summary, "Caption length", "Mean engagement by caption length", output_dir / "caption_length.png")

    observations = [
        f"{len(hashtag_summary)} unique hashtags appear; {int(hashtag_summary['post_count'].sum())} tagged-post occurrences were counted.",
        f"Most common hashtag is {hashtag_summary.index[0]} (n={int(hashtag_summary.iloc[0]['post_count'])}; mean ER {hashtag_summary.iloc[0]['mean_er']:.2%})." if len(hashtag_summary) else "No hashtags were present.",
        f"Caption length is measured in words; {int(df['caption'].fillna('').str.split().str.len().median())} words is the median.",
    ]
    lines = ["# Text analysis", "", "Hashtag and caption patterns are descriptive associations in this dataset; they do not show that text causes engagement.", ""]
    lines.extend(f"- {observation}" for observation in observations)
    lines.extend(["", "## Hashtag engagement", "", "![Mean engagement by common hashtag](./hashtag_text.png)", "", "## Caption length", "", "![Mean engagement by caption length](./caption_length.png)", ""])
    (output_dir / "text_analysis_summary.md").write_text("\n".join(lines), encoding="utf-8")
    return observations


if __name__ == "__main__":
    from src.analysis import REP, load

    for item in analyze_text(load(), REP):
        print(f"- {item}")
