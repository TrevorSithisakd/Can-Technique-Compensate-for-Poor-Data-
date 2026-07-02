# creating the feature sets
import pandas as pd

def build_label(close, horizon) -> pd.DataFrame:
    # label is percentage return
    return close.shift(-horizon) / close - 1

def build_features(close, feature_set) -> pd.DataFrame:
    if feature_set == "baseline":
        feats = {
            "mom_21":   close.pct_change(21),
            "mom_63":   close.pct_change(63),
            "mom_126":  close.pct_change(126),
            "mom_252":  close.pct_change(252),
            "mom_12_1": close.shift(21) / close.shift(252) - 1,
        }
    else:
        raise ValueError(f"unknown feature_set: {feature_set!r}")

    return pd.DataFrame({name: df.stack() for name, df in feats.items()})

def build_dataset(close, feature_set="baseline", horizon=FORWARD_DAYS) ->pd.DataFrame:
    # i think this is just combining the two datasets together 
    y = build_label(close, horizon).stack() # original is wide stack to create (date, ticker)
    X = build_features(close, feature_set)
    ds = X.join(y, how="inner")
    return ds.dropna()