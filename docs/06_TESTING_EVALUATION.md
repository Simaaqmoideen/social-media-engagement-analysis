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
| 2026-10-27 | `python src/analysis.py`; `python -m pytest -q`; `git diff --check` | Six chart files, `chart_takeaways.md`, and `post_rankings.csv` created. Grouped counts for type/hour/weekday/hashtag-count each sum to 600; top/bottom rankings contain 20 distinct posts; 7 tests passed. Highest synthetic mean ER: video 8.54%; highest hour: 18:00 at 10.25% (n=21). | Must-have segmentation and chart coverage plus the Should-have top/bottom ranking are present; results are descriptive and do not establish causes. |
| 2026-10-27 | `python src/text_analysis.py`; `python -m pytest -q`; `git diff --check` | Text analysis created two charts and two CSV summaries; hashtag counts reconcile to 1,215 occurrences, caption buckets reconcile to 600 posts; 8 tests passed. | Hashtag frequency and caption-length summaries are reproducible; no sentiment result is reported because VADER could not be installed offline. |
| 2026-10-27 | `python src/model.py`; `python -m pytest -q` | Seeded 80/20 holdout: 480 train / 120 test. Baseline MAE 0.02318, RMSE 0.02904; regression MAE 0.01782, RMSE 0.02263, R² 0.3927; 9 tests passed. | Regression beats the mean predictor on this holdout. Coefficients rank associations in this synthetic dataset and should not be interpreted causally. |
| 2026-10-28 | `python -m py_compile dashboard.py src/model.py src/text_analysis.py`; `python -m pytest -q`; `git diff --check` | Dashboard syntax check passed; 9 tests passed. Attempted Streamlit app smoke test, but sandbox socket permissions blocked HTTP access to localhost. | App source is syntactically valid; confirm interactive rendering by launching `streamlit run dashboard.py` in a normal local environment. |
