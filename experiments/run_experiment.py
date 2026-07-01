"""Shared entry point every experiment script calls.

One function does data -> model -> walk-forward predictions; a second scores
and logs them. Experiments A, B, and C are all just loops over these two,
varying whichever axis (model, feature_set, years, universe, horizon) that
experiment is testing. No new framework -- this is the thin wrapper the
research plan calls for.

Depends on (not yet implemented -- fill these in, this file's calls define
the expected interface):
  data.py       - load_features(tickers, start, end, feature_set) -> DataFrame
                  (long format: one row per date x ticker, feature columns + actual_return)
  models.py     - get_model(name) -> estimator with .fit(X, y) / .predict(X)
  validation.py - walk_forward(df, model, feature_cols, forward_days, min_train_years)
                  -> predictions DataFrame (date, ticker, predicted_return, actual_return)
  evaluation.py - compute_metrics(pred_df) -> {ic, t_stat, ci_low, ci_high, sharpe, dir_acc}
"""

import mlflow

import data
import models
import validation
import evaluation

MLFLOW_EXPERIMENT = "compensate-for-poor-data"


def get_predictions(model_name, feature_cols, tickers, start, end, forward_days=5, min_train_years=3):
    """data -> model -> walk-forward predictions. Reused by run_experiment and by
    Experiment C, which needs the raw predictions (not just the scored metrics)
    to build its permutation null."""
    df = data.load_features(tickers, start, end, feature_cols)
    model = models.get_model(model_name)
    return validation.walk_forward(df, model, feature_cols, forward_days, min_train_years)


def run_experiment(model_name, feature_cols, tickers, start, end, forward_days=5, min_train_years=3):
    """Run one (model, feature_set, data-slice) cell, score it, log it to MLflow.

    Returns params + metrics merged into one dict, so callers just append the
    result to a list and build a DataFrame -- no separate results store needed,
    MLflow already keeps the full run history.
    """
    preds = get_predictions(model_name, feature_cols, tickers, start, end, forward_days, min_train_years)
    metrics = evaluation.compute_metrics(preds)

    params = {
        "model": model_name,
        "feature_set": ",".join(feature_cols),
        "n_tickers": len(tickers),
        "start": start,
        "end": end,
        "forward_days": forward_days,
    }

    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics({k: v for k, v in metrics.items() if isinstance(v, (int, float))})

    return {**params, **metrics}


def demo():
    # ponytail: smallest runnable check. Real coverage needs data/models/validation/
    # evaluation to exist first -- this just guards the signatures don't rot silently.
    import inspect
    assert list(inspect.signature(get_predictions).parameters) == [
        "model_name", "feature_cols", "tickers", "start", "end", "forward_days", "min_train_years",
    ]
    assert list(inspect.signature(run_experiment).parameters) == list(
        inspect.signature(get_predictions).parameters
    )
    print("run_experiment scaffold OK")


if __name__ == "__main__":
    demo()
