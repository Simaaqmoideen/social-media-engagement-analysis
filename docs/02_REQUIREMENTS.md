# Requirements: Social Media Data Analysis

## Functional requirements (MoSCoW)

### Must have
- [x] Load posts data (date, type, caption, likes, comments, shares, followers)
- [x] Compute engagement rate = (likes + comments + shares) / followers; use zero for zero followers
- [ ] Analyse by post type, hour of day, day of week and hashtag
- [ ] At least 5 clear charts and a written list of insights

### Should have
- [ ] Sentiment analysis of captions or comments (VADER)
- [ ] Top and bottom 10 posts with reasons
- [ ] Simple regression to rank drivers of engagement
- [ ] Interactive dashboard

### Could have (stretch)
- [ ] Topic modelling on captions
- [ ] Pull real data via platform APIs (respect terms of service)
- [ ] Word clouds
- [ ] Compare multiple accounts

## Non-functional requirements
- **Reproducible:** a fresh clone runs end to end with the commands in README.md.
- **Secure:** secrets only in `.env`; no keys, tokens or personal data in Git.
- **Readable:** type hints on public functions, docstrings on modules, PEP 8 formatting.
- **Tested:** automated tests for core logic; they pass before every merge.
- **Documented:** README and docs updated whenever behaviour changes.

## Assumptions
- Python 3.10 or newer; internet access to install packages and fetch data.
- Free-tier / free-dataset resources are used wherever possible.

## Constraints
- Solo or small-team student project; target is a working demo, not production.
