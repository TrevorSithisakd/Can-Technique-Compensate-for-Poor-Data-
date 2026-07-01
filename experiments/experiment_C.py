"""Experiment C -- is any of it real?

Take the single best config (from A/B), get its raw walk-forward predictions,
then compare its measured IC against a permutation null: shuffle actual_return
within each date and recompute IC ~1000x. The p-value is the honest verdict
on H1 -- does anything here beat chance.
"""

import numpy as np
import pandas as pd

from run_experiment import get_predictions
import evaluation

# TODO: set these from Experiment A/B's winning config
BEST_MODEL, BEST_FEATURES = "ridge", ["momentum", "technical", "macro", "cross_sectional"]
TICKERS = []  # TODO: same universe used to pick the winner
START, END = "2018-01-01", "2023-12-31"

N_PERMUTATIONS = 1000


def permutation_null(pred_df: pd.DataFrame, n: int = N_PERMUTATIONS, seed: int = 0) -> np.ndarray:
    """Shuffle actual_return within each date (preserves the cross-section on
    each day, destroys any real predictive link), recompute IC, repeat n times.
    This is the noise floor every measured IC gets compared against."""
    rng = np.random.default_rng(seed)
    null_ics = np.empty(n)
    for i in range(n):
        shuffled = pred_df.copy()
        shuffled["actual_return"] = shuffled.groupby("date")["actual_return"].transform(
            lambda s: rng.permutation(s.values)
        )
        null_ics[i] = evaluation.information_coefficient(
            shuffled["predicted_return"].values, shuffled["actual_return"].values
        )
    return null_ics


def run():
    preds = get_predictions(BEST_MODEL, BEST_FEATURES, TICKERS, START, END)
    measured_ic = evaluation.information_coefficient(
        preds["predicted_return"].values, preds["actual_return"].values
    )
    null_ics = permutation_null(preds)
    p_value = float(np.mean(null_ics >= measured_ic))
    return measured_ic, null_ics, p_value


if __name__ == "__main__":
    measured_ic, null_ics, p_value = run()
    print(f"measured IC: {measured_ic:.4f}")
    print(f"null mean/std: {null_ics.mean():.4f} / {null_ics.std():.4f}")
    print(f"p-value: {p_value:.4f}")
