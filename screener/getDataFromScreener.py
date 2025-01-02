import csv
import json
import argparse
import sys
import requests_cache
import yfinance as yf
import pandas as pd

from icecream import ic
from time import sleep
from itertools import islice
from datetime import datetime
from dateutil.relativedelta import relativedelta

# input_file = "data/StocksTrendingAbove10emaForMonth260524.csv"
# input_file = "../data/sample_screener_name/2024.06.08.csv"
# input_file = "../data/all-emas-in-all-candles-trending_22_12_2024.csv"
session = requests_cache.CachedSession('yfinance.cache',
                                       expire_after=86400)  # Cache expiration: 1 day
session.headers['User-agent'] = 'vicky-program/2.0'

def get_price_change_percentage(ticker_symbol, start_date):
   # Fetch historical data
    tickers = yf.Tickers(ticker_symbol,
                         session=session)
    stock = tickers.tickers.get(ticker_symbol)
    # Fetch historical data
    historical_data = stock.history(period="max")
    # start_date = '-'.join(val for val in start_date.split('-')[::-1])
    specific_date_close = historical_data.loc[start_date]["Close"]
    # Ensure data exists
    if not specific_date_close:
        return f"No data available for {ticker_symbol} since {start_date}"
    # Get the starting and current prices as scalars
    start_price = round(specific_date_close, 2)  # This gives the first value
    current_price = historical_data["Close"].iloc[-1] # Get the latest date

    # Calculate the percentage change
    change_percentage = ((current_price - start_price) / start_price) * 100

    return round(change_percentage, 2)

def get_all_stock_details(input_file):
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        stock_details = {}
        stock_date_details = {}
        for row in csv_reader:
            if line_count:
                # Get details based on stocks
                stock_date, stock_name = row[0], row[1]
                if stock_details.get(stock_name):
                    stock_details[stock_name].append(stock_date)
                else:
                    stock_details[stock_name] = [stock_date]
                # Get details based on date
                if stock_date_details.get(stock_date):
                    stock_date_details[stock_date].append(stock_name)
                else:
                    stock_date_details[stock_date] = [stock_name]
                line_count += 1
            else:
                line_count += 1
        return stock_details, stock_date_details


def get_appearance_count(stocks_data, date_details, current_date):
    stocks_count_details = {}
    ic(index)
    current_date = list_of_date[index]
    ic(current_date)
    for stock in stocks_data:
        count = 0
        if current_date in stocks_data[stock]:
            date_index = stocks_data[stock].index(current_date)
            if date_index == 0:
                count = 1
            # If stock appearing after a week, consider it as new
            else:
                last_found_date = stocks_data[stock][date_index-1]
                # Convert from string to datetime format
                date_format = "%d-%m-%Y"
                last_found_date_obj =datetime.strptime(last_found_date, date_format)
                current_date_obj = datetime.strptime(current_date, date_format)
                difference = relativedelta(current_date_obj,
                                           last_found_date_obj)
                if difference.days > 20:
                    print("There is a difference of a week.")
                    count = 1
        stocks_count_details[stock] = count
    # stocks_count_details[stock] = count
    # print('stocks_count_details :', stocks_count_details)
    return stocks_count_details


def get_new_stocks(count_data):
    new_stocks = list()
    for stock in count_data:
        if (count_data[stock] == 1):
            new_stocks.append(stock)
    return new_stocks


def sort_based_on_appearance_count(data, sorted_dates, top=10):
    high_trending_stocks = {}
    sorted_dict = dict(
        sorted(data.items(), key=lambda item: len(item[1]), reverse=True))
    high_appearance_stocks = {k: len(v) for k, v in
                              dict(islice(sorted_dict.items(),
                                          top)
                                   ).items()
                              }
    for stock, count in high_appearance_stocks.items():
        if stock in sorted_dates[-1][1]:
            high_trending_stocks[stock] = count
    return high_trending_stocks

'''
def create_urls(stocks):
    if isinstance(stocks, list):
        return construct_urls(stocks)
    elif isinstance(stocks, dict):
        return construct_urls(stocks.keys())
'''

def construct_urls(stock):
    return (f"https://chartink.com/stocks/{stock.lower()}.html")


def input_args():
    parser = argparse.ArgumentParser('Provide inputs for screener data')
    parser.add_argument('--input-csvs-file',
                        help='Input csvs files')
    parser.add_argument('--input-file',
                        help='Input screener file')
    parser.add_argument('--history-days', type=int,
                        default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = input_args()
    single_csv_file = args.input_file
    history_days = args.history_days
    csv_files_input = args.input_csvs_file
    if ((csv_files_input and single_csv_file) or csv_files_input):
        with open(csv_files_input) as fd:
            csv_data = json.load(fd)
        csv_files = csv_data.get('csvs')
    elif (not csv_files_input and single_csv_file):
        csv_files = [single_csv_file]
    else:
        print('Provide valid input csv files')
        sys.exit(1)
    for screener_file in csv_files:
        print(f'\n------screener file: {screener_file} ---------\n')
        stocks_data, date_details = get_all_stock_details(screener_file)
        # ic(date_details)
        # ic(stocks_data)
        # ic(date_details.keys())
        # ic(list(date_details.values())[:3])
        sorted_date_details = sorted(date_details.items(),
                                     key=lambda x: datetime.strptime(x[0],
                                     '%d-%m-%Y'))
        # ic(type(sorted_date_details))
        # ic(sorted_date_details)
        # ic(stocks_data)
        # ic(sorted_date_details)
        if not history_days:
            history_days = len(date_details)
        # ic(history_days)
        list_of_date = list(date_details.keys())
        for index in range(1, history_days-1):
            # date = list_of_date[index]
            # ic(date)
            ic(index)
            current_date = list_of_date[index]

            count_details = get_appearance_count(stocks_data,
                                                 date_details,
                                                 current_date)
            # ic(count_details)
            new_stocks = get_new_stocks(
                count_details)
            date_format = '-'.join(val for val in current_date.split('-')[::-1])
            print(f'Newly found stocks {
                  index} days ago on {current_date}: {new_stocks}')
            for stock in new_stocks:
                print(f'\t{construct_urls(stock)}')
                # sleep(2)
                try:
                    change_percent = get_price_change_percentage(f'{stock}.NS',
                                                             date_format)
                except KeyError as err:
                    print(f'Got {err} for {stock}')
                    change_percent = -1000
                print('\tChange % Since:', change_percent)

        # Sort more trending stocks
        # TODO :Get value of top from user, currently 10
        high_trending_stocks = sort_based_on_appearance_count(stocks_data,
                                                             sorted_date_details,
                                                             top=100)
        print('\nhigh_trending_stocks :', high_trending_stocks)
        # for stock in high_trending_stocks:
        #     print(f'\t{construct_urls(stock)}')
        #
