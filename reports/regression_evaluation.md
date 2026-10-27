# Regression evaluation

Random holdout: 480 training posts and 120 test posts (random_state=7).
The baseline predicts the training-set mean engagement rate. Predictors are post type, weekday, posting hour, hashtag count and caption word count.
Coefficients describe linear associations in this synthetic dataset; they do not establish causes. The random split is for this non-time-series demo.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| training_mean_baseline | 0.0232 | 0.0290 | -0.0006 |
| linear_regression | 0.0178 | 0.0226 | 0.3927 |

## Driver ranking

Mean absolute standardized coefficient by feature family (larger magnitude means stronger fitted association within this model):

- type: 0.0160
- hour: 0.0067
- n_tags: 0.0041
- weekday: 0.0030
- caption_words: 0.0001
