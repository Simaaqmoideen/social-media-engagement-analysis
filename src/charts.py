"""Create charts and sample-aware takeaways for exploratory engagement analysis."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from src.analysis import extract_hashtags


WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CHART_FILES = {
    "distribution": "engagement_distribution.png",
    "post_type": "by_type.png",
    "hour": "by_hour.png",
    "weekday": "by_weekday.png",
    "hashtag_count": "by_n_tags.png",
    "hashtag": "by_hashtag.png",
}


def engagement_groups(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return mean engagement and sample counts for each required breakdown."""
    tag_rows = df.assign(tag=df["hashtags"].apply(extract_hashtags)).explode("tag")
    tag_rows = tag_rows.dropna(subset=["tag"])
    return {
        "post_type": df.groupby("type")["er"].agg(["mean", "count"]).sort_values("mean", ascending=False),
        "hour": df.groupby("hour")["er"].agg(["mean", "count"]).reindex(range(24)),
        "weekday": df.groupby("weekday")["er"].agg(["mean", "count"]).reindex(WEEKDAY_ORDER),
        "hashtag_count": df.groupby("n_tags")["er"].agg(["mean", "count"]),
        "hashtag": tag_rows.groupby("tag")["er"].agg(["mean", "count"]).sort_values("mean", ascending=False),
    }


def _save_bar(summary: pd.DataFrame, title: str, output: Path) -> None:
    """Save a mean-rate bar chart and include group sample sizes."""
    labels = [f"{key}\n(n={int(count)})" for key, count in zip(summary.index, summary["count"])]
    fig, axis = plt.subplots(figsize=(9, 4.5))
    bars = axis.bar(labels, summary["mean"], color="#3569a8")
    axis.set_title(title)
    axis.set_ylabel("Mean engagement rate")
    axis.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axis.grid(axis="y", alpha=0.2)
    axis.bar_label(bars, labels=[f"{value:.1%}" for value in summary["mean"]], padding=3)
    axis.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def _takeaways(df: pd.DataFrame, groups: dict[str, pd.DataFrame]) -> list[str]:
    """Make dataset-specific descriptive statements for the chart pack."""
    median = df["er"].median()
    q1, q3 = df["er"].quantile([0.25, 0.75])
    hour = groups["hour"].dropna()
    weekday = groups["weekday"].dropna()
    n_tags = groups["hashtag_count"].dropna()
    top_type = groups["post_type"].iloc[0]
    top_hashtag = groups["hashtag"].iloc[0]
    return [
        f"Median engagement is {median:.2%}; the middle half of posts ranges from {q1:.2%} to {q3:.2%}.",
        f"{groups['post_type'].index[0]} posts have the highest mean rate ({top_type['mean']:.2%}; n={int(top_type['count'])}).",
        f"The strongest observed hour is {int(hour['mean'].idxmax()):02d}:00 ({hour['mean'].max():.2%}; n={int(hour.loc[hour['mean'].idxmax(), 'count'])}).",
        f"{weekday['mean'].idxmax()} has the highest mean rate by weekday ({weekday['mean'].max():.2%}; n={int(weekday.loc[weekday['mean'].idxmax(), 'count'])}).",
        f"Posts with {int(n_tags['mean'].idxmax())} hashtags have the highest mean by hashtag count ({n_tags['mean'].max():.2%}; n={int(n_tags.loc[n_tags['mean'].idxmax(), 'count'])}).",
        f"{groups['hashtag'].index[0]} has the highest observed hashtag mean ({top_hashtag['mean']:.2%}; n={int(top_hashtag['count'])}).",
    ]


def rank_posts(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Return top and bottom posts with descriptive context, not causal claims."""
    ranked = df.copy()
    ranked["ranking"] = ""
    top_indices = set(ranked.nlargest(limit, "er").index)
    bottom_indices = set(ranked.loc[~ranked.index.isin(top_indices)].nsmallest(limit, "er").index)
    ranked.loc[list(top_indices), "ranking"] = "Top"
    ranked.loc[list(bottom_indices), "ranking"] = "Bottom"
    ranked = ranked[ranked["ranking"].ne("")].copy()
    ranked["descriptive_context"] = ranked.apply(
        lambda row: (
            f"{row['type']} post at {int(row['hour']):02d}:00 on {row['weekday']}; "
            f"{int(row['n_tags'])} hashtags; {row['likes'] + row['comments'] + row['shares']} total interactions"
        ),
        axis=1,
    )
    return ranked[["ranking", "post_id", "timestamp", "type", "er", "likes", "comments", "shares", "followers", "descriptive_context"]].sort_values(
        ["ranking", "er"], ascending=[True, False]
    ).reset_index(drop=True)


def create_chart_pack(df: pd.DataFrame, output_dir: Path) -> list[str]:
    """Save six EDA charts and a Markdown takeaway for each chart."""
    output_dir.mkdir(parents=True, exist_ok=True)
    groups = engagement_groups(df)

    fig, axis = plt.subplots(figsize=(9, 4.5))
    axis.hist(df["er"], bins=30, color="#3569a8", edgecolor="white")
    axis.set(title="Distribution of post engagement rates", xlabel="Engagement rate", ylabel="Posts")
    axis.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axis.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(output_dir / CHART_FILES["distribution"], dpi=150)
    plt.close(fig)

    titles = {
        "post_type": "Mean engagement by post type",
        "hour": "Mean engagement by posting hour",
        "weekday": "Mean engagement by weekday",
        "hashtag_count": "Mean engagement by hashtag count",
        "hashtag": "Mean engagement by hashtag",
    }
    for name, title in titles.items():
        _save_bar(groups[name], title, output_dir / CHART_FILES[name])

    takeaways = _takeaways(df, groups)
    section_names = ["Engagement distribution", "Post format", "Posting hour", "Weekday", "Number of hashtags", "Hashtag"]
    lines = ["# Chart takeaways", "", "These findings describe associations in this dataset; they do not establish causes.", ""]
    for section, filename, takeaway in zip(section_names, CHART_FILES.values(), takeaways):
        lines.extend([f"## {section}", "", f"![{section}](./{filename})", "", takeaway, ""])
    (output_dir / "chart_takeaways.md").write_text("\n".join(lines), encoding="utf-8")
    rankings = rank_posts(df)
    rankings.to_csv(output_dir / "post_rankings.csv", index=False)
    return takeaways
