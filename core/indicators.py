from collections import deque
import numpy as np
import pandas as pd

def sma_sliding_window(values: pd.Series, k: int) -> pd.Series:
    """
    O(n) simple moving average using a true sliding window.
    Only emits a value when the window has k non-NaN points.
    """
    n = len(values)
    out = [np.nan] * n
    window = deque()
    window_sum = 0.0
    valid_count = 0

    for i, x in enumerate(values):
        window.append(x)
        if pd.notna(x):
            window_sum += float(x)
            valid_count += 1

        if len(window) > k:
            old = window.popleft()
            if pd.notna(old):
                window_sum -= float(old)
                valid_count -= 1

        if len(window) == k and valid_count == k:
            out[i] = window_sum / k

    return pd.Series(out, index=values.index, name=f"SMA_{k}")

def daily_simple_returns(close: pd.Series) -> pd.Series:
    """r_t = (P_t - P_{t-1}) / P_{t-1}"""
    return close.pct_change().rename("Daily_Return")
