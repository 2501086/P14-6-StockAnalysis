import pandas as pd

def find_up_down_runs(close: pd.Series):
    """
    Close-to-close changes:
      - Up day: diff > 0
      - Down day: diff < 0
      - Flat/NaN breaks a run
    Returns:
      runs: list of dicts {start, end, direction, length}
      summary: dict with counts, totals, longest for up/down
    """
    diff = close.diff()
    runs = []
    direction = None  # 'up' or 'down'
    start_idx = None
    length = 0

    for i in range(1, len(diff)):
        d = diff.iloc[i]
        current_dir = 'up' if pd.notna(d) and d > 0 else ('down' if pd.notna(d) and d < 0 else None)

        if current_dir is None:
            if direction is not None:
                runs.append({
                    "start": close.index[start_idx],
                    "end": close.index[i-1],
                    "direction": direction,
                    "length": length
                })
                direction, start_idx, length = None, None, 0
            continue

        if direction is None:
            direction = current_dir
            start_idx = i
            length = 1
        elif current_dir == direction:
            length += 1
        else:
            runs.append({
                "start": close.index[start_idx],
                "end": close.index[i-1],
                "direction": direction,
                "length": length
            })
            direction = current_dir
            start_idx = i
            length = 1

    if direction is not None and length > 0:
        runs.append({
            "start": close.index[start_idx],
            "end": close.index[-1],
            "direction": direction,
            "length": length
        })

    up_runs = [r for r in runs if r["direction"] == "up"]
    down_runs = [r for r in runs if r["direction"] == "down"]

    summary = {
        "up": {
            "num_runs": len(up_runs),
            "total_days_in_runs": sum(r["length"] for r in up_runs),
            "longest_streak": max([r["length"] for r in up_runs], default=0),
        },
        "down": {
            "num_runs": len(down_runs),
            "total_days_in_runs": sum(r["length"] for r in down_runs),
            "longest_streak": max([r["length"] for r in down_runs], default=0),
        }
    }
    return runs, summary
