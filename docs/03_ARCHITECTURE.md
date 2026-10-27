# Architecture: Social Media Data Analysis

## Overview
```
Posts CSV (real export or synthetic)
        |
        v
 src/clean.py  -> parse dates, drop duplicates, handle nulls
        |
        v
 src/analysis.py -> engagement rate, groupbys, hashtags
        |
        v
 src/charts.py -> reports/*.png + reports/chart_takeaways.md
        |
        v
 (optional) dashboard.py
```

## Tech stack
- Python 3.10+
- pandas, numpy
- matplotlib / seaborn
- vaderSentiment (optional)
- scikit-learn
- Streamlit or Power BI (optional dashboard)
- pytest

## Design decisions (fill in as you go)
| Decision | Options considered | Choice | Why |
|---|---|---|---|
| Engagement rate | Divide interactions by followers; handle zero followers as missing or zero | `(likes + comments + shares) / followers`, or zero when followers is zero | Matches project definition and avoids division by zero. |
| Missing text | Drop post, keep null, or empty string | Keep post and fill caption/hashtag text with empty strings | A missing hashtag list means no observed tags; preserve valid engagement observations. |
| Duplicate post ID | Keep first or aggregate duplicate export rows | Keep first occurrence | Export duplicate rows should not inflate counts or engagement summaries. |
| Descriptive summary | Raw list of extrema or show sample size | Report means with group sample counts and descriptive caveat | Small groups should be interpreted in context; association is not causation. |

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
