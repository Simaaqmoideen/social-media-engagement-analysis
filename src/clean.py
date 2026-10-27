"""Validate and clean exported or synthetic social media post records."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "posts.csv"
CLEAN_PATH = ROOT / "data" / "posts_clean.csv"
REQUIRED_COLUMNS = {
    "post_id", "timestamp", "type", "caption", "hashtags",
    "followers", "likes", "comments", "shares",
}
COLUMN_ORDER = [
    "post_id", "timestamp", "type", "caption", "hashtags", "followers",
    "likes", "comments", "shares",
]
COUNT_COLUMNS = ["followers", "likes", "comments", "shares"]


def clean_posts(posts: pd.DataFrame) -> pd.DataFrame:
    """Return validated posts, removing invalid rows and duplicate post IDs.

    Missing caption and hashtag text is represented as an empty string. Rows
    missing a post ID or parseable timestamp, containing invalid or negative
    audience/interaction counts, or lacking a post type are dropped. A zero
    follower count is retained; its engagement rate is defined as zero.
    Duplicate post IDs keep the first row in input order.
    """
    missing_columns = REQUIRED_COLUMNS - set(posts.columns)
    if missing_columns:
        raise ValueError(f"Posts data is missing columns: {sorted(missing_columns)}")

    cleaned = posts[COLUMN_ORDER].copy()
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"], errors="coerce")
    for column in COUNT_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned["type"] = cleaned["type"].astype("string").str.strip()
    cleaned["caption"] = cleaned["caption"].fillna("").astype(str)
    cleaned["hashtags"] = cleaned["hashtags"].fillna("").astype(str)

    valid = (
        cleaned["post_id"].notna()
        & cleaned["timestamp"].notna()
        & cleaned["type"].notna()
        & cleaned["type"].ne("")
        & cleaned[COUNT_COLUMNS].notna().all(axis=1)
        & cleaned[COUNT_COLUMNS].ge(0).all(axis=1)
    )
    cleaned = cleaned.loc[valid].drop_duplicates("post_id", keep="first")
    cleaned["post_id"] = cleaned["post_id"].astype(str)
    cleaned[COUNT_COLUMNS] = cleaned[COUNT_COLUMNS].astype("int64")
    return cleaned.sort_values(["timestamp", "post_id"]).reset_index(drop=True)


def load_posts(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load a raw post CSV and return cleaned records."""
    return clean_posts(pd.read_csv(path))


def main() -> None:
    """Write a clean copy and print a reproducible data-quality summary."""
    raw = pd.read_csv(RAW_PATH)
    clean = clean_posts(raw)
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(CLEAN_PATH, index=False)
    print(f"Raw rows: {len(raw):,}; cleaned rows: {len(clean):,}; removed: {len(raw) - len(clean):,}")
    print(f"Date range: {clean['timestamp'].min()} to {clean['timestamp'].max()}")
    print(f"Post types: {clean['type'].value_counts().to_dict()}")
    print(f"Missing caption text: {(clean['caption'] == '').sum():,}")
    print(f"Missing hashtag text: {(clean['hashtags'] == '').sum():,}")
    print(f"Zero-follower posts: {(clean['followers'] == 0).sum():,}")
    print(f"Saved cleaned data to {CLEAN_PATH}")


if __name__ == "__main__":
    main()
