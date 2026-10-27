"""Synthetic posts for one account -> data/posts.csv"""
import pathlib
import numpy as np, pandas as pd

rng = np.random.default_rng(7)
N = 600
types = rng.choice(["image", "video", "carousel", "text"], N, p=[0.35, 0.3, 0.2, 0.15])
ts = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 365 * 24, N), unit="h")
hour = ts.hour
tags_pool = ["#ai", "#coding", "#study", "#tips", "#career", "#python", "#fun", "#news"]
tags = [" ".join(rng.choice(tags_pool, rng.integers(0, 5), replace=False)) for _ in range(N)]
followers = (5000 + np.arange(N) * 8).astype(int)
type_mult = pd.Series(types).map({"video": 1.6, "carousel": 1.3, "image": 1.0, "text": 0.7}).values
hour_mult = 1 + 0.5 * np.exp(-((hour - 19) ** 2) / 8)
tag_mult = 1 + 0.08 * np.array([min(len(t.split()), 3) for t in tags])
base = followers * 0.035 * type_mult * hour_mult * tag_mult
likes = rng.poisson(base * rng.lognormal(0, 0.35, N))
comments = rng.poisson(likes * 0.06)
shares = rng.poisson(likes * 0.04)
captions = rng.choice(["Loved building this!", "Quick tips you need", "This is terrible, avoid", "Amazing results today", "Not sure about this one", "Big news incoming"], N)
df = pd.DataFrame({"post_id": range(N), "timestamp": ts, "type": types, "caption": captions, "hashtags": tags,
                   "followers": followers, "likes": likes, "comments": comments, "shares": shares})
out = pathlib.Path(__file__).resolve().parents[1] / "data"; out.mkdir(exist_ok=True)
df.sort_values("timestamp").to_csv(out / "posts.csv", index=False)
print("wrote", out / "posts.csv")
