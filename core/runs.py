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
    #find the difference in price of closing days
    runs = []
    #just a list to store runs
    direction = None  # 'up' or 'down'
    start_idx = None
    length = 0
    #direction is the direction of the ongoing run only changes when run changes
    #current_dir is the direction of the stock daily changes everyday

    for i in range(1, len(diff)):
        #go through each day, starting from 1 since day 0 will have no diff
        d = diff.iloc[i]
        #diff. means get the difference of the .iloc = interger location gets the value of position i
        current_dir = 'up' if pd.notna(d) and d > 0 else ('down' if pd.notna(d) and d < 0 else None)
        #if d is not a nan and is greater then 0 then consider it as 'up' under current_dir variable same for down and if not either is counted as None 

        if current_dir is None:
            #if todays direction is none then we need to close it and see if previous days were up or down so the next code is will close the direction run
            if direction is not None:
                runs.append({
                    "start": close.index[start_idx],
                    #date that run began
                    "end": close.index[i-1],
                    #date that run close
                    "direction": direction,
                    #what is the direction:up or down
                    "length": length
                    #number of days in the run
                })
                direction, start_idx, length = None, None, 0
                #this resets it so direction = None, start_idx = None, length = 0
            continue
        #skip the rest of the loop since doesnt satisfy the other conditions

        if direction is None:
            #if the main direction is None means reseted yesterday and starting a new run
            direction = current_dir
            #direction is equal to current_dir so if current_dir is up direction will be up
            start_idx = i
            length = 1

        elif current_dir == direction:
            length += 1
            #if the current_dir is already the same as direction lenght plus one

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
            #if not reset the code run

    # after loop ends, if a run is still open, close it to include the tail
    if direction is not None and length > 0:
        runs.append({
            "start": close.index[start_idx],  # start date of the last run
            "end": close.index[-1],           # end date is the last available date in data
            "direction": direction,           # final run direction
            "length": length                  # final run length
        })

    # split runs into up and down using list comprehension
    up_runs = [r for r in runs if r["direction"] == "up"]
    # [ ... for r in runs if condition ] = build a new list by filtering items from runs

    down_runs = [r for r in runs if r["direction"] == "down"]

    # build a summary dictionary with counts, totals, and longest streak
    summary = {
        "up": {
            "num_runs": len(up_runs),                              # len() = count number of up runs
            "total_days_in_runs": sum(r["length"] for r in up_runs),  # sum() = add up lengths of all up runs
            "longest_streak": max([r["length"] for r in up_runs], default=0),  # max() = biggest length (0 if none)
        },
        "down": {
            "num_runs": len(down_runs),                                # count number of down runs
            "total_days_in_runs": sum(r["length"] for r in down_runs), # total days across down runs
            "longest_streak": max([r["length"] for r in down_runs], default=0), # longest down run
        }
    }

    return runs, summary
    # return both the detailed runs list and the summary stats
