import pandas as pd

def max_profit_multiple_transactions(close: pd.Series) -> float:
    """
    Leetcode 122 — sum of all positive day-to-day gains.
    """
    diffs = close.diff()
    return float(diffs[diffs > 0].sum(skipna=True))
