# file to get ohlcv data from yfinanance
import yfinance as yf
import pandas as pd
from config import TICKERS, START_DATE, END_DATE
import os
import hashlib 
# cachecing 
# check if cache exists
# if not make the folder

# from config import the ticker list to see what needs to be downloaded 
CACHE_DIR   = "./cache"

def _cache_file() -> str:
    # Ticker universe baked into cached file to save on duplicate recomputation
    key = ",".join(sorted(TICKERS)) + START_DATE + END_DATE
    tag = hashlib.md5(key.encode()).hexdigest()[:8]
    return os.path.join(CACHE_DIR, f"prices_{tag}.csv")

def load_prices() -> pd.DataFrame:
    # check if cache exists 
    path = _cache_file() # gets current associated file path if it exists by checking what corresponding id it would be from the hash encoding
    if os.path.exists(path):
        print(f"Loading cached data from {path}")
        raw = pd.read_csv(path, header=[0,1], index_col=0, parse_dates=True)
        return raw 
    print(f"Downloading OHLCV for {len(TICKERS)} tickers ({START_DATE}–{END_DATE})")
    raw = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=True, progress=False)
    os.makedirs(CACHE_DIR, exist_ok=True)
    raw.to_csv(path)

    return raw

def load_close() -> pd.DataFrame:
    # close prices for whole universe dates + tickers 
    raw = load_prices()
    tickers = raw.columns.get_level_values(1).unique()
    return pd.concat([_extract_close(raw, t) for t in tickers], axis=1)

def _extract_close(raw, ticker_symbol: str) -> pd.Series:
    """Helper to pull a single close series from a yfinance multi or single download."""
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"][ticker_symbol]
    else:
        close = raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.rename(ticker_symbol)

# load spy 

# load macro data 

# earning dates

# eaarning surprise??