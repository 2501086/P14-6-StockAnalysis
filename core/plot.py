import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict

def plot_price_sma_and_runs(df: pd.DataFrame, sma_col: str, runs: List[Dict], title: str):
    """
    - Line plot: Close and SMA
    - Shaded regions for up/down runs (green/red)
    """
    close = df["Close"]
    sma = df[sma_col]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(close.index, close.values, label="Close")
    ax.plot(sma.index, sma.values, label=sma_col)

    for r in runs:
        color = "green" if r["direction"] == "up" else "red"
        ax.axvspan(r["start"], r["end"], alpha=0.15, color=color)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()
