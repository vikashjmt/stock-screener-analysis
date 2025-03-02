import csv
import json
import argparse
import os
import sys
import time
import pytz
import requests_cache
import yfinance as yf
import pandas as pd
import numpy as np

from icecream import ic
from itertools import islice
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# input_file = "data/StocksTrendingAbove10emaForMonth260524.csv"
# input_file = "../data/sample_screener_name/2024.06.08.csv"
# input_file = "../data/all-emas-in-all-candles-trending_22_12_2024.csv"
session = requests_cache.CachedSession('yfinance.cache',
                                       expire_after=86400)  # Cache expiration: 1 day
session.headers['User-agent'] = 'vicky-program/2.0'
os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()  # Apply the timezone change in Linux (used by GitHub Actions)
pytz.timezone("Asia/Kolkata")


def get_price_change_percentage(ticker_symbol, start_date, tickers):
    # Fetch historical data
    # tickers = yf.Tickers(ticker_symbol,
    #                      session=session)
    # Fetch historical data
    # Convert start_date to pandas datetime
    start_date_pd = pd.to_datetime(start_date)
    historical_data = tickers[ticker_symbol]
    # Convert DataFrame index to datetime if not already
    historical_data.index = pd.to_datetime(historical_data.index)
    # start_date = '-'.join(val for val in start_date.split('-')[::-1])
    try:
        specific_date_close = historical_data.loc[start_date_pd]["Close"]
    except KeyError:
        print(f"Date {start_date} not found in data, using the last available close price.")
        if not historical_data.empty:
            #specific_date_close = historical_data['Close'].iloc[-1]
            specific_date_close = historical_data.loc[historical_data.index.asof(start_date_pd), "Close"]
        else:
            print("Historical data is empty.")
            return -1000
    if np.isnan(specific_date_close):
        start_date_pd = update_date_if_market_holiday(start_date)
        specific_date_close = historical_data.loc[start_date_pd]["Close"]
    # Get the starting and current prices as scalars
    start_price = round(specific_date_close, 2)  # This gives the first value
    current_price = historical_data["Close"].iloc[-1]  # Get the latest date

    # Calculate the percentage change
    change_percentage = ((current_price - start_price) / start_price) * 100
    return float(round(change_percentage, 2))


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
    # ic(index)
    current_date = list_of_date[index]
    # ic(current_date)
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
                try:
                    date_format = "%d-%m-%Y %I:%M %p"
                    last_found_date_obj = datetime.strptime(last_found_date.strip(),
                                                            date_format)
                except:
                    date_format = "%d-%m-%Y"
                    last_found_date_obj = datetime.strptime(last_found_date.strip(), date_format)
                current_date_obj = datetime.strptime(current_date, date_format)
                difference = relativedelta(current_date_obj,
                                           last_found_date_obj)
                if difference.days > 20:
                    # ic("There is a difference of a month.")
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


def sort_based_on_change_percent(data):
    # high_percent_stocks = {}
    sorted_dict = dict(
        sorted(data.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict

# Define market holidays (weekends or specific holidays)


def update_date_if_market_holiday(date_str):
    """
    Checks if a given date is a market holiday (weekend or predefined holiday).
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Weekends (Saturday, Sunday)
    # Add predefined market holidays (example: New Year's Day, Independence Day, etc.)
    market_holidays = {

        # Add other holidays here...
    }
    if (date_obj.date() in market_holidays
            or date_obj.weekday() in (5, 6)):
        date_obj = date_obj - timedelta(days=2)
        return date_obj.strftime('%Y-%m-%d')
    else:
        return date_str

def get_stocks_price_data(stocks_data, start_date, end_date):
    '''
    stocks_price_data = {}
    tickers = yf.Tickers(' '.join(f'{stock}.NS' for stock in stocks_data),
                         session=session)
    for stock in stocks_data:
        stock = tickers.tickers.get(f'{stock}.NS')
        historical_data = stock.history(period="max")
        stocks_price_data[f'{stock}.NS'] = historical_data
    return stocks_price_data
    '''
    # Join stock symbols with ".NS" and fetch all data in one request
    tickers = ' '.join(f'{stock}.NS' for stock in stocks_data)
    # Fetch historical data for all stocks at once
    historical_data = yf.download(tickers, session=session, group_by="ticker",
                                  start=start_date, end=end_date)
    historical_data.to_csv('historical_data.csv')
    downloaded_stocks = list(historical_data.columns.levels[0])

    # print("Failed Downloads:", failed_tickers)
    # Process the data into a dictionary
    stocks_price_data = {}
    for stock in stocks_data:
        stock_ticker = f'{stock}.NS'
        if stock_ticker in historical_data:
            stocks_price_data[stock_ticker] = historical_data[stock_ticker]

    return stocks_price_data


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
    for index, screener_file in enumerate(csv_files):
        print(f'\n{index+1}) Screener file: {screener_file}\n')
        stocks_data, date_details = get_all_stock_details(screener_file)
        # ic(date_details)
        # ic(stocks_data)
        list_of_date = list(date_details.keys())
        # ic(list_of_date)
        # start_date = list_of_date[0]
        start_date = '-'.join(val for val in list_of_date[0].split('-')[::-1])
        # ic(start_date)
        # end_date = list_of_date[-1]
        end_date = '-'.join(val for val in list_of_date[-1].split('-')[::-1])
        # ic(end_date)
        tickers = get_stocks_price_data(stocks_data.keys(), start_date,
                                        end_date)
        stock_price_data = {}
        total_days = len(date_details)
        if not history_days:
            history_days = total_days
        # ic(history_days)
        list_of_date = list(date_details.keys())
        for index in range(total_days-history_days, total_days):
            # date = list_of_date[index]
            # ic(date)
            # ic(index)
            current_date = list_of_date[index]
            # TODO : Optimize it later
            # Calling twice to avoid rare case of Friday to be holiday
            # current_date = update_date_if_market_holiday(current_date)
            ic(current_date)
            count_details = get_appearance_count(stocks_data,
                                                 date_details,
                                                 current_date)
            # ic(count_details)
            new_stocks = get_new_stocks(
                count_details)
            date_format = '-'.join(val for val in current_date.split('-')
                                   [::-1])
            if new_stocks:
                print(
                    f'\n{total_days - index} interval ago on {current_date}, new stocks found:')
            for index, stock in enumerate(new_stocks):
                print(f'    {index + 1}. {stock}:')
                print(f'\tURL: {construct_urls(stock)}')
                # time.sleep(2)
                try:
                    change_percent = get_price_change_percentage(f'{stock}.NS',
                                                                 date_format,
                                                                 tickers)
                    if np.isnan(change_percent):
                        # print('\t\tChange_percent is nan')
                        change_percent = -500
                except KeyError as err:
                    print(f'\tGot {err} for {stock}')
                    change_percent = -1000
                if not stock_price_data.get(stock):
                    stock_price_data[stock] = change_percent
                print('\tChange % Since:', change_percent)
        # ic(stock_price_data)
        high_percent_change_stocks = sort_based_on_change_percent(
            stock_price_data)
        print('Higher % stocks:')
        for stock, change in high_percent_change_stocks.items():
            print(f'\t- {stock}: {change}%')
        # Sort more trending stocks
        # TODO :Get value of top from user, currently 10
        '''
        high_trending_stocks = sort_based_on_appearance_count(stocks_data,
                                                             sorted_date_details,
                                                             top=100)
        print('\nhigh_trending_stocks :', high_trending_stocks)
        '''
        # for stock in high_trending_stocks:
        #     print(f'\t{construct_urls(stock)}')
        #
