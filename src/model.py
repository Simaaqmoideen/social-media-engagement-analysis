"""Compare a held-out mean baseline with a simple engagement regression."""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = ["hour", "n_tags", "caption_words"]
CATEGORICAL_FEATURES = ["type", "weekday"]


def model_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Build leak-free predictors and target from cleaned posts."""
    features = df[["hour", "n_tags", *CATEGORICAL_FEATURES]].copy()
    features["caption_words"] = df["caption"].fillna("").str.split().str.len()
    return features, df["er"].astype(float)


def evaluate_regression(
    df: pd.DataFrame, output_dir: Path, test_size: float = 0.2, random_state: int = 7
) -> dict[str, object]:
    """Evaluate regression against a training-mean baseline on held-out posts."""
    features, target = model_frame(df)
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=random_state
    )
    preprocessing = ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])
    model = Pipeline([("preprocess", preprocessing), ("regression", LinearRegression())])
    model.fit(x_train, y_train)
    baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)
    prediction = model.predict(x_test)
    baseline_prediction = baseline.predict(x_test)

    metrics = pd.DataFrame([
        {"model": "training_mean_baseline", "mae": mean_absolute_error(y_test, baseline_prediction),
         "rmse": mean_squared_error(y_test, baseline_prediction) ** 0.5, "r2": r2_score(y_test, baseline_prediction)},
        {"model": "linear_regression", "mae": mean_absolute_error(y_test, prediction),
         "rmse": mean_squared_error(y_test, prediction) ** 0.5, "r2": r2_score(y_test, prediction)},
    ])

    names = model.named_steps["preprocess"].get_feature_names_out()
    coefficients = pd.DataFrame({"feature": names, "coefficient": model.named_steps["regression"].coef_})
    def feature_group(name: str) -> str:
        prefix, value = name.split("__", maxsplit=1)
        return value if prefix == "numeric" else value.split("_", maxsplit=1)[0]

    coefficients["feature_group"] = coefficients["feature"].map(feature_group)
    drivers = (
        coefficients.assign(abs_coefficient=coefficients["coefficient"].abs())
        .groupby("feature_group")["abs_coefficient"].mean().sort_values(ascending=False)
        .rename("mean_absolute_standardized_coefficient").reset_index()
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_dir / "regression_metrics.csv", index=False)
    coefficients.to_csv(output_dir / "regression_coefficients.csv", index=False)
    drivers.to_csv(output_dir / "regression_driver_ranking.csv", index=False)
    lines = [
        "# Regression evaluation", "",
        f"Random holdout: {len(x_train)} training posts and {len(x_test)} test posts (random_state={random_state}).",
        "The baseline predicts the training-set mean engagement rate. Predictors are post type, weekday, posting hour, hashtag count and caption word count.",
        "Coefficients describe linear associations in this synthetic dataset; they do not establish causes. The random split is for this non-time-series demo.", "",
        "| Model | MAE | RMSE | R² |", "|---|---:|---:|---:|",
    ]
    for row in metrics.itertuples(index=False):
        lines.append(f"| {row.model} | {row.mae:.4f} | {row.rmse:.4f} | {row.r2:.4f} |")
    lines.extend(["", "## Driver ranking", "", "Mean absolute standardized coefficient by feature family (larger magnitude means stronger fitted association within this model):", ""])
    lines.extend(f"- {row.feature_group}: {row.mean_absolute_standardized_coefficient:.4f}" for row in drivers.itertuples(index=False))
    (output_dir / "regression_evaluation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"metrics": metrics, "drivers": drivers, "train_rows": len(x_train), "test_rows": len(x_test)}


if __name__ == "__main__":
    import pathlib
    import sys

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from src.analysis import REP, load

    result = evaluate_regression(load(), REP)
    print(result["metrics"].to_string(index=False))
    print("\nDriver ranking:")
    print(result["drivers"].to_string(index=False))
