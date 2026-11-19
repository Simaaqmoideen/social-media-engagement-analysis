"""Thin Streamlit dashboard for exploring the synthetic posts dataset."""

import streamlit as st
import pandas as pd
from src.clean import RAW_PATH

from src.analysis import load
from src.charts import rank_posts
from src.text_analysis import text_summaries, caption_sentiment_summary


st.set_page_config(page_title="Social Media Analysis", page_icon="📊", layout="wide")
st.title("Social Media Engagement Explorer")
st.caption("Exploratory associations in the included synthetic dataset; not causal guidance.")

@st.cache_data(ttl=300)
def load_dashboard_posts(source_mtime: float) -> pd.DataFrame:
    """Cache the cleaned source data and refresh when the CSV changes."""
    return load()


posts = load_dashboard_posts(RAW_PATH.stat().st_mtime)
types = st.sidebar.multiselect("Post types", sorted(posts["type"].unique()), default=sorted(posts["type"].unique()))
date_bounds = (posts["timestamp"].min().date(), posts["timestamp"].max().date())
selected_dates = st.sidebar.date_input("Publication date range", value=date_bounds, min_value=date_bounds[0], max_value=date_bounds[1])
if len(selected_dates) == 2:
    start, end = selected_dates
    posts = posts[
        posts["timestamp"].dt.date.between(start, end) & posts["type"].isin(types)
    ]
else:
    posts = posts[posts["type"].isin(types)]

if posts.empty:
    st.info("No posts match these filters. Adjust the sidebar selections.")
    st.stop()

posts = posts.copy()
posts["interactions"] = posts["likes"] + posts["comments"] + posts["shares"]
median_er = posts["er"].median()
cols = st.columns(4)
cols[0].metric("Posts", f"{len(posts):,}")
cols[1].metric("Mean engagement", f"{posts['er'].mean():.2%}")
cols[2].metric("Median engagement", f"{median_er:.2%}")
cols[3].metric("Interactions", f"{posts['interactions'].sum():,}")

overview, text, sentiment, rankings = st.tabs(["Engagement", "Text", "Caption sentiment", "Top and bottom posts"])
with overview:
    left, right = st.columns(2)
    by_type = posts.groupby("type", as_index=False)["er"].mean().sort_values("er", ascending=False)
    by_weekday = posts.groupby("weekday", as_index=False)["er"].mean()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_weekday["weekday"] = pd.Categorical(by_weekday["weekday"], categories=weekday_order, ordered=True)
    by_weekday = by_weekday.sort_values("weekday")
    left.subheader("Mean engagement by post type")
    left.bar_chart(by_type, x="type", y="er", alt="Mean engagement rate by post format")
    right.subheader("Mean engagement by weekday")
    right.bar_chart(by_weekday, x="weekday", y="er", alt="Mean engagement rate by weekday")
    by_hour = posts.groupby("hour", as_index=False)["er"].mean().sort_values("hour")
    st.subheader("Mean engagement by posting hour")
    st.line_chart(by_hour, x="hour", y="er", alt="Mean engagement rate by posting hour")

with text:
    hashtag_summary, caption_summary = text_summaries(posts)
    left, right = st.columns(2)
    left.subheader("Hashtag frequency and engagement")
    left.dataframe(hashtag_summary.rename(columns={"mean_er": "Mean engagement", "post_count": "Posts"}), width="stretch", alt="Hashtag counts and mean engagement rates")
    right.subheader("Caption length and engagement")
    right.dataframe(caption_summary.rename(columns={"mean_er": "Mean engagement", "post_count": "Posts"}), width="stretch", alt="Caption length groups and mean engagement rates")

with sentiment:
    sentiment_summary = caption_sentiment_summary(posts)
    st.subheader("VADER sentiment in captions")
    st.caption("Lexicon-based sentiment labels are approximate and may miss sarcasm, context, or domain-specific language.")
    st.bar_chart(sentiment_summary.reset_index(), x="sentiment", y="mean_er", alt="Mean engagement rate by VADER caption sentiment")
    st.dataframe(sentiment_summary, width="stretch", alt="Caption sentiment counts, mean engagement, and mean VADER score")

with rankings:
    selected = rank_posts(posts)
    st.dataframe(selected, width="stretch", hide_index=True, alt="Top and bottom posts with descriptive context")
    st.caption("Post rankings summarize observed outcomes; descriptive context is not an explanation of causality.")
