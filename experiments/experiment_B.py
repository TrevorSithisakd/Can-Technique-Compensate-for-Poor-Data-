"""Experiment B -- does data quantity/quality help? (the headline experiment)

Fix model + features at Experiment A's winner, plus the plain momentum+ridge
baseline for contrast, then move only the data axis: lookback years, universe
size, horizon. Three separate 1D sweeps rather than a full cross product --
each axis answers its own question and a 5x4x3 cross product buys nothing
extra here.
"""

import pandas as pd
from run_experiment import run_experiment

# TODO: set these from Experiment A's winning cell
BEST_MODEL, BEST_FEATURES = "ridge", ["momentum", "technical", "macro", "cross_sectional"]
BASELINE_MODEL, BASELINE_FEATURES = "ridge", ["momentum"]

CONFIGS = [
    (BEST_MODEL, BEST_FEATURES, "best"),
    (BASELINE_MODEL, BASELINE_FEATURES, "baseline"),
]

FULL_TICKERS = []  # TODO: universe ranked by market cap, once data.py exists
END = "2023-12-31"  # 2024 hold-out stays untouched

YEARS_GRID = [1, 2, 3, 5, 7]
UNIVERSE_GRID = [10, 50, 100, 500]
HORIZON_GRID = [1, 5, 20]


def sweep_years():
    rows = []
    for years in YEARS_GRID:
        start = f"{int(END[:4]) - years}-01-01"
        for model, features, tag in CONFIGS:
            r = run_experiment(model, features, FULL_TICKERS, start, END)
            r.update(axis="years", value=years, config=tag)
            rows.append(r)
    return rows


def sweep_universe():
    rows = []
    for n in UNIVERSE_GRID:
        for model, features, tag in CONFIGS:
            r = run_experiment(model, features, FULL_TICKERS[:n], "2018-01-01", END)
            r.update(axis="universe", value=n, config=tag)
            rows.append(r)
    return rows


def sweep_horizon():
    rows = []
    for h in HORIZON_GRID:
        for model, features, tag in CONFIGS:
            r = run_experiment(model, features, FULL_TICKERS, "2018-01-01", END, forward_days=h)
            r.update(axis="horizon", value=h, config=tag)
            rows.append(r)
    return rows


def run():
    return pd.DataFrame(sweep_years() + sweep_universe() + sweep_horizon())


if __name__ == "__main__":
    table = run()
    table.to_csv("experiments/results_experiment_B.csv", index=False)
    print(table.groupby(["axis", "value", "config"])["ic"].mean())
