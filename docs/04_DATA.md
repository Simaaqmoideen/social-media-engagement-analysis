# Data: Social Media Data Analysis

## Sources
- Kaggle: search 'Instagram posts engagement' or 'Twitter sentiment' datasets.
- Your own exported analytics (Instagram / YouTube Studio / LinkedIn) if you manage an account.
- Included: `python src/generate_data.py` builds a realistic synthetic dataset (post type, hour, hashtags, captions) for offline use.

## Data handling rules
- Raw data is never edited by hand. Cleaning is done by code and written to a new file.
- Large files are not committed (see `.gitignore`); document how to download them instead.
- Respect each dataset's licence and terms of service; cite the source in the final report.
- Do not store personal or sensitive information unless it is anonymised.

## Data dictionary (fill in after loading the data)
| Column | Type | Meaning | Missing values? |
|---|---|---|---|
| post_id | string | Stable post identifier; duplicate IDs keep the first row | No after cleaning |
| timestamp | datetime | Post publication timestamp | Invalid or missing timestamps are dropped |
| type | string | Post format (image, video, carousel, text) | Missing or blank type is dropped |
| caption | string | Caption text | Missing values become empty strings |
| hashtags | string | Space-separated hashtags | Missing values become empty strings |
| followers | integer | Follower count at publication | Invalid/negative rows are dropped; zero is retained |
| likes | integer | Like count | Invalid/negative rows are dropped |
| comments | integer | Comment count | Invalid/negative rows are dropped |
| shares | integer | Share count | Invalid/negative rows are dropped |

The default generated file contains 600 synthetic posts dated 2024-01-02
through 2024-12-29. The 111 missing hashtag strings are treated as posts with
no hashtag text. `python src/clean.py` writes a separate, reproducible cleaned
copy to the git-ignored `data/posts_clean.csv`; raw data is not edited.
Engagement rate is `(likes + comments + shares) / followers`, with a zero
rate when followers is zero to avoid division by zero.

## Data quality checklist
- [x] Row count and column types checked
- [x] Missing values counted and a handling decision recorded
- [x] Duplicates removed
- [x] Outliers and impossible values reviewed (negative counts rejected; zero followers retained and rate set to zero)
- [x] Train / test split strategy written down (not applicable to descriptive EDA; no predictive evaluation in scope)
