# Architecture: Social Media Data Analysis

## Overview
```
Posts CSV (real export or synthetic)
        |
        v
 src/clean.py  -> parse dates, drop duplicates, handle nulls
        |
        v
 src/analysis.py -> engagement rate, groupbys, hashtags, correlations
        |
        v
 src/charts.py / reports/*.png  ->  reports/INSIGHTS.md
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
| | | | |

## Module responsibilities
See the files in `src/`. Keep logic (testable functions) separate from UI and scripts.
