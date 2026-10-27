# Testing and Evaluation: Social Media Data Analysis

## Success metrics
- 5+ charts, each with a one-sentence takeaway
- 3+ actionable recommendations
- Findings reproducible by running one script

## Test plan
- [ ] Unit: engagement-rate function handles zero followers
- [ ] Unit: hashtag extractor handles no hashtags and repeated tags
- [ ] Check: group totals add up to the dataset total
- [ ] Manual: peer review of INSIGHTS.md for unsupported claims

## How to run tests
```bash
python -m pytest -q
```

## Results log
| Date | Experiment / test | Result | Conclusion |
|---|---|---|---|
| 2026-10-27 | `python src/generate_data.py`; `python src/clean.py`; `python -m pytest -q` | 600 rows generated for 2024-01-02 to 2024-12-29; 0 duplicate post IDs; 0 missing required values; 111 missing hashtag strings filled as empty strings; 0 rows removed; 5 tests passed. | Synthetic input is reproducible and the cleaning pipeline preserves valid posts while handling absent hashtags and invalid rows explicitly. |
