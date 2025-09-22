# Or run: python -m stock_trend_analysis.main
from core.data import get_numeric_close
from core.indicators import sma_sliding_window, daily_simple_returns
from core.runs import find_up_down_runs
from core.strategy import max_profit_multiple_transactions
from core.plot import plot_price_sma_and_runs

import pandas as pd

# -------- Config (edit these) --------
TICKER = "AAPL"
PERIOD = "1y"
INTERVAL = "1d"
SMA_WINDOW = 5
# -------------------------------------

def main():
    # 1) Data
    close = get_numeric_close(TICKER, PERIOD, INTERVAL)
    data = pd.DataFrame({"Close": close})

    # 2) Indicators
    sma_series = sma_sliding_window(data["Close"], SMA_WINDOW)
    data[sma_series.name] = sma_series
    data["Daily_Return"] = daily_simple_returns(data["Close"])

    # 3) Runs + summary
    runs, summary = find_up_down_runs(data["Close"])

    # 4) Strategy: max profit
    profit = max_profit_multiple_transactions(data["Close"])

    # 5) Print summary
    print(f"\n=== {TICKER} | {PERIOD} | {INTERVAL} ===")
    print(f"SMA window: {SMA_WINDOW}")
    print("\nUp/Down Runs Summary:")
    print(f"  Up   -> num_runs: {summary['up']['num_runs']}, "
          f"total_days: {summary['up']['total_days_in_runs']}, "
          f"longest_streak: {summary['up']['longest_streak']}")
    print(f"  Down -> num_runs: {summary['down']['num_runs']}, "
          f"total_days: {summary['down']['total_days_in_runs']}, "
          f"longest_streak: {summary['down']['longest_streak']}")
    print(f"\nMax Profit (multiple transactions): {profit:.2f}")

    # 6) Plot
    plot_price_sma_and_runs(
        data,
        sma_series.name,
        runs,
        title=f"{TICKER} Close vs. {sma_series.name} (shaded up/down runs)"
    )

if __name__ == "__main__":
    main()
