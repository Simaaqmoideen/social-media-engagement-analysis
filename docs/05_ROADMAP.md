# Roadmap: Social Media Data Analysis

Suggested pace: one phase every 2-4 days (about 2-3 weeks in total).

## Phase 1: Setup and data
Obtain data, inspect columns, missing values and outliers. Define engagement rate precisely.

- [x] Task completed
- [x] Notes written in the project log
- [x] Changes committed

## Phase 2: EDA
Distributions, top posts, engagement by type / hour / weekday.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Phase 3: Text analysis
Hashtag frequency versus engagement, caption length, optional sentiment.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Phase 4: Modelling (light)
Regression or correlation matrix to rank drivers. Be careful to say 'associated with', not 'causes'.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Phase 5: Storytelling
Write `INSIGHTS.md` with 5+ recommendations backed by charts. Optional dashboard.

- [ ] Task completed
- [ ] Notes written in the project log
- [ ] Changes committed

## Project log
| Date | What I did | Blockers | Next |
|---|---|---|---|
| 2026-10-27 | Generated and inspected the synthetic dataset; added a reusable cleaning pipeline, cleaned-copy output, and engagement-rate data handling. Raw 600 rows had no duplicate IDs or missing required values; 111 hashtag strings were empty and retained as no tags. Cleaned all 600 rows. `python -m pytest -q`: 5 passed. | None. | Phase 2: quantify engagement patterns and build the required chart pack. |
