import json
import argparse

from pathlib import Path
from icecream import ic
from datetime import date
watchlist_file = Path("watch_list.json")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='Add a stock to watchlist')
    parser.add_argument('--add-stocks', type= str,
                       nargs ='+',
                       help='Add list of stocks to watchlist',
                       required=False)
    parser.add_argument('--remove-stocks', type= str,
                       nargs ='+',
                       help='Add list of stocks to watchlist',
                       required=False)
    args = parser.parse_args()
    args_val = vars(args)
    ic(args)
    stocks_to_add = args_val['add_stocks']
    stocks_to_remove = args_val['remove_stocks']
    ic(stocks_to_add)
    if Path.exists(watchlist_file):
        with open(watchlist_file) as fd:
            watch_list = json.load(fd)
    else:
        watch_list = {}

    today = date.today().strftime('%d-%m-%Y')
    ic(today)

    # Add stocks to watchlist
    if stocks_to_add:
        for stock_name in stocks_to_add:
            watch_list[stock_name] = today

    # Remove stocks from watchlist
    if stocks_to_remove:
        for stock_name in stocks_to_remove:
            del watch_list[stock_name]
    # Update the watchlist to watchlist file
    with open(watchlist_file,'w') as fd:
        json.dump(watch_list, fd, indent=4)
