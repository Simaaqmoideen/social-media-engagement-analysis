# Project 5: Social Media Data Analysis

> Analyze likes, comments and posts to understand what content works and why people engage.

**What you will learn:** Exploratory data analysis, engagement metrics, text and hashtag analysis, sentiment, correlation versus causation, and storytelling with charts.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/generate_data.py
python src/clean.py
python src/analysis.py
python src/text_analysis.py
python src/model.py
```
Run the tests with `python -m pytest -q` from this folder.

The analysis command saves six chart images and chart-specific takeaways under
`reports/` after validating and cleaning the input. The takeaways describe
associations in this synthetic sample, not causal effects.
The text-analysis command writes hashtag frequency and caption-length summaries
and charts to `reports/`.
The modeling command compares a mean baseline with linear regression on a held-out
test split and writes metrics and coefficient summaries to `reports/`.

## Folder map
| Path | Purpose |
|---|---|
| `docs/01_PROJECT_BRIEF.md` | Problem, users, scope, success criteria |
| `docs/02_REQUIREMENTS.md` | Must / should / could requirements and non-functional needs |
| `docs/03_ARCHITECTURE.md` | Design, components, tech stack |
| `docs/04_DATA.md` | Data sources, schema and data rules |
| `docs/05_ROADMAP.md` | Phase-by-phase build plan with checklists |
| `docs/06_TESTING_EVALUATION.md` | Test plan and evaluation metrics |
| `docs/07_RISKS_ETHICS.md` | Risks, mitigations, ethics notes |
| `docs/08_DELIVERABLES_CHECKLIST.md` | Definition of done |
| `docs/09_REPORT_TEMPLATE.md` | Final report / presentation outline |
| `src/` | Starter source code |
| `tests/` | Automated tests |
| `data/` | Datasets (git-ignored except samples) |
| `notebooks/` | Exploration notebooks |
| `reports/` | Generated charts and metrics |

## Tech stack
- Python 3.10+
- pandas, numpy
- matplotlib / seaborn
- vaderSentiment (optional)
- scikit-learn
- Streamlit or Power BI (optional dashboard)
- pytest
