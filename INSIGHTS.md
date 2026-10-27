# Social media analysis: findings and experiment ideas

The following results describe the included 600-post synthetic dataset. They are hypotheses to test with authorized account data, not claims about real audiences or causes.

## Observations

- The median engagement rate is 5.58%, with the middle 50% between 4.08% and 7.74%.
- Video posts have the highest mean engagement rate (8.54%, 187 posts) among the four formats.
- Posts published at 18:00 have the highest hourly mean (10.25%, 21 posts); the small group size makes this estimate less stable.
- Sunday has the highest weekday mean (6.67%, 74 posts).
- Posts with three hashtags have the highest mean by hashtag-count group (7.24%, 123 posts). The `#ai` group has the highest per-hashtag mean (7.06%, 148 occurrences).
- Captions of 5–9 words have a 6.75% mean rate (102 posts), compared with 6.20% for 0–4 words (498 posts). There are no 10+ word captions in this generated sample.
- The regression improved test MAE from 0.02318 for the training-mean baseline to 0.01782 on a 120-post holdout. Type, hour and hashtag count had the largest grouped absolute standardized coefficients. R² was 0.3927.

## Recommendations to validate

1. **Run a format experiment.** Pair comparable topics and publishing windows, then randomize video versus image/carousel where practical. Video led the synthetic sample, but this is not evidence that a real audience will respond the same way.
2. **Test an early-evening slot.** Compare 18:00 with the account's normal posting time over multiple weeks. The 18:00 group contained only 21 synthetic posts, so treat the observed peak as an experiment candidate.
3. **Compare hashtag counts in matched posts.** Test three relevant tags against the account's usual number while holding format and topic as steady as possible; the observed 3-tag mean was highest in this dataset.
4. **Trial concise captions.** Compare short and 5–9 word captions on similar posts, since the 5–9 word group had a higher synthetic mean. The generated sample has no long captions, so it cannot inform longer-copy performance.
5. **Use a controlled weekly schedule test.** The Sunday mean was highest, but weekday composition, content and sample sizes may differ. Rotate comparable content across days before changing the calendar.

## Interpretation limits

The data generator deliberately assigns engagement patterns to format, hour and hashtag count. These findings primarily show that the analysis pipeline recovers patterns in simulated data. The regression is an exploratory model, not a validated forecasting system. Use privacy-safe, authorized real data and preplanned experiments before acting on these ideas.
