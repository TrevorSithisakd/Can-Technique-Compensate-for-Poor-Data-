"""Experiment A -- does technique help?

Hold data fixed (full pre-hold-out window, 2018-2023; 2024 stays untouched
until final evaluation). Cross two axes independently in the same grid:

  - same feature_set, vary model  -> isolates model sophistication
  - same model, vary feature_set  -> isolates feature sophistication

Every (model x feature_set) cell runs through run_experiment -- a grid, not
one model per experiment -- so the result table can be sliced either way:
row-wise for "does a better model help", column-wise for "do more features help".
"""

import pandas as pd
from run_experiment import run_experiment

TICKERS = []  # TODO: populate once data.py defines the ticker universe
START, END = "2018-01-01", "2023-12-31"  # pre-hold-out window only; 2024 is untouched

MODELS = ["mean", "ridge", "random_forest", "xgboost"]  # complexity ladder, cheapest first

FEATURE_SETS = {
    "momentum_only":    ["momentum"],
    "+technical":       ["momentum", "technical"],
    "+macro":           ["momentum", "technical", "macro"],
    "+cross_sectional": ["momentum", "technical", "macro", "cross_sectional"],
    "+fundamentals":    ["momentum", "technical", "macro", "cross_sectional", "fundamentals"],
}


def run():
    rows = []
    for feature_name, feature_cols in FEATURE_SETS.items():
        for model_name in MODELS:
            result = run_experiment(model_name, feature_cols, TICKERS, START, END)
            result["feature_set_name"] = feature_name
            rows.append(result)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = run()
    table.to_csv("experiments/results_experiment_A.csv", index=False)
    print(table.pivot(index="feature_set_name", columns="model", values="ic"))
