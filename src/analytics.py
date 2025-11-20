"""
analytics.py
------------
Mathematical tools for pairs trading:
- static OLS hedge ratio
- dynamic rolling hedge ratio
- spread construction
- z-score computation
- ADF test of cointegration
- analysis pipelines (static + dynamic)
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def compute_static_beta(x: pd.Series, y: pd.Series) -> float:
    """
    Compute the hedge ratio β via OLS: x = α + βy + ε.
    Returns a single number (constant beta).
    """
    X = sm.add_constant(y)
    model = sm.OLS(x, X).fit()
    beta = model.params[1]
    return beta

def compute_dynamic_beta(x: pd.Series, y: pd.Series, window: int = 60) -> pd.Series:
    """
    Compute dynamic rolling hedge ratio β_t = Cov(x,y)/Var(y)
    using a rolling window. Returns a time series.
    """
    cov = x.rolling(window).cov(y)
    var = y.rolling(window).var()
    beta = cov / var
    return beta

def compute_spread(x: pd.Series, y: pd.Series, beta) -> pd.Series:
    """
    Compute spread = x - βy.
    beta can be float (static) or a Series (dynamic).
    """
    return x - beta * y

def compute_zscore(series: pd.Series, window: int = 60) -> pd.Series:
    """
    Compute rolling z-score of a series.
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    z = (series - mean) / std
    return z

def adf_test(series: pd.Series):
    """
    Apply ADF test to check cointegration (mean-reversion).
    Returns the p-value.
    """
    series = series.dropna()
    result = adfuller(series)
    p_value = result[1]
    return p_value

def analyze_pair_static(df: pd.DataFrame, x: str, y: str, window: int = 60):
    """
    Full static analysis for pair (x,y):
    - compute constant beta via OLS
    - spread
    - z-score
    - ADF test
    """
    X = df[x]
    Y = df[y]

    beta = compute_static_beta(X, Y)
    spread = compute_spread(X, Y, beta)
    zscore = compute_zscore(spread, window)
    p_value = adf_test(spread)

    return {
        "beta": beta,
        "spread": spread,
        "zscore": zscore,
        "adf_p": p_value
    }

def analyze_pair_dynamic(df: pd.DataFrame, x: str, y: str, window: int = 60):
    """
    Full dynamic analysis for pair (x,y):
    - rolling hedge ratio β_t
    - dynamic spread
    - z-score
    - ADF test on entire spread series
    """
    X = df[x]
    Y = df[y]

    beta_series = compute_dynamic_beta(X, Y, window)
    spread = compute_spread(X, Y, beta_series)
    zscore = compute_zscore(spread, window)
    p_value = adf_test(spread)

    return {
        "beta": beta_series,
        "spread": spread,
        "zscore": zscore,
        "adf_p": p_value
    }


