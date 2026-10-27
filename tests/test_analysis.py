from src.analysis import engagement_rate, extract_hashtags
from src.clean import clean_posts
from src.charts import engagement_groups, rank_posts
from src.text_analysis import text_summaries
import pandas as pd
from src.analysis import load


def test_engagement_rate():
    assert engagement_rate(80, 15, 5, 1000) == 0.1


def test_zero_followers():
    assert engagement_rate(1, 1, 1, 0) == 0.0


def test_hashtags():
    assert extract_hashtags("Hi #AI #ai #Py") == ["#ai", "#py"]
    assert extract_hashtags("no tags") == []
    assert extract_hashtags(None) == []


def test_clean_posts_fills_missing_text_and_deduplicates_ids():
    posts = pd.DataFrame({
        "post_id": [1, 1, 2],
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "type": ["image", "video", "text"],
        "caption": [None, "duplicate", "caption"],
        "hashtags": [None, "#ignored", "#ai"],
        "followers": [100, 100, 0],
        "likes": [3, 99, 1],
        "comments": [1, 0, 0],
        "shares": [0, 0, 0],
    })
    clean = clean_posts(posts)
    assert clean["post_id"].tolist() == ["1", "2"]
    assert clean.iloc[0]["caption"] == ""
    assert clean.iloc[0]["hashtags"] == ""


def test_clean_posts_drops_negative_count_rows():
    posts = pd.DataFrame({
        "post_id": [1], "timestamp": ["2024-01-01"], "type": ["image"],
        "caption": ["ok"], "hashtags": [""], "followers": [100],
        "likes": [-1], "comments": [0], "shares": [0],
    })
    assert clean_posts(posts).empty


def test_required_group_totals_match_analyzed_posts():
    posts = load()
    groups = engagement_groups(posts)
    for key in ["post_type", "hour", "weekday", "hashtag_count"]:
        assert int(groups[key]["count"].sum()) == len(posts)


def test_post_rankings_include_ten_distinct_top_and_bottom_posts():
    ranked = rank_posts(load())
    assert ranked["ranking"].value_counts().to_dict() == {"Top": 10, "Bottom": 10}
    assert ranked["post_id"].nunique() == 20
    assert ranked["descriptive_context"].notna().all()


def test_text_summaries_cover_tagged_occurrences_and_all_caption_groups():
    posts = load()
    hashtag_summary, caption_summary = text_summaries(posts)
    tagged_occurrences = sum(len(tags) for tags in posts["hashtags"].apply(extract_hashtags))
    assert hashtag_summary["post_count"].sum() == tagged_occurrences
    assert set(caption_summary.index.astype(str)) == {"0-4 words", "5-9 words", "10+ words"}
    assert caption_summary["post_count"].sum() == len(posts)
