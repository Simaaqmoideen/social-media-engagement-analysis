# Roadmap: Social Media Data Analysis

Suggested pace: one phase every 2-4 days (about 2-3 weeks in total).

## Phase 1: Setup and data
Obtain data, inspect columns, missing values and outliers. Define engagement rate precisely.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 2: EDA
Distributions, top posts, engagement by type / hour / weekday.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 3: Text analysis
Hashtag frequency versus engagement, caption length, optional sentiment.

- [x] Task completed (hashtag and caption analysis)
- [x] Notes written in the project log
- [x] Changes committed

## Phase 4: Modelling (light)
Regression or correlation matrix to rank drivers. Be careful to say 'associated with', not 'causes'.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 5: Storytelling
Write `INSIGHTS.md` with 5+ recommendations backed by charts. Optional dashboard.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Project log
| Date | What I did | Blockers | Next |
|---|---|---|---|
| 2026-10-27 | Generated and inspected the synthetic dataset; added a reusable cleaning pipeline, cleaned-copy output, and engagement-rate data handling. Raw 600 rows had no duplicate IDs or missing required values; 111 hashtag strings were empty and retained as no tags. Cleaned all 600 rows. `python -m pytest -q`: 5 passed. | None. | Phase 2: quantify engagement patterns and build the required chart pack. |
| 2026-10-27 | Added six charts (engagement distribution, post type, hour, weekday, hashtag count, hashtag), sample-aware takeaways, and top/bottom 10 posts with descriptive context. For the synthetic sample, video mean ER is 8.54%; 18:00 is highest by hour at 10.25% (n=21); required group counts reconcile to 600 posts. `python src/analysis.py` created six charts; `python -m pytest -q`: 7 passed. | None. | Phase 3: analyze hashtag and caption-text relationships with engagement. |
| 2026-10-27 | Added hashtag frequency and caption-length summaries, plots and text-analysis report. The synthetic sample has 8 unique hashtags, 1,215 tagged-post occurrences and a 3-word median caption; `python -m pytest -q`: 8 passed. VADER sentiment remains unchecked because the dependency is not installed and package download failed in the offline environment. | VADER sentiment needs an available package install to run and verify. | Phase 4: fit and interpret a simple engagement regression. |
| 2026-10-27 | Compared a training-mean baseline with linear regression on a seeded 80/20 holdout (480 train, 120 test). Test MAE improved from 0.02318 to 0.01782; RMSE from 0.02904 to 0.02263; regression R²=0.3927. Type, hour and hashtag count ranked highest by mean absolute standardized coefficient. `python -m pytest -q`: 9 passed. | None for regression; optional sentiment remains unavailable offline. | Phase 5: write evidence-backed recommendations and final report. |
| 2026-10-28 | Added five testable recommendations, completed the final report, and built a type/date-filterable Streamlit dashboard. README now documents workflow, commands, sample results and a Mermaid diagram. Unit tests: 9 passed. Dashboard syntax checked; local browser smoke test was blocked by sandbox socket restrictions. | Interactive UI could not be opened in this sandbox; optional VADER sentiment remains unavailable offline. | Complete; use README commands to run the dashboard locally. |
