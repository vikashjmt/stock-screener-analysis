import csv
import json
import argparse

from icecream import ic
from itertools import islice
from datetime import datetime

# input_file = "data/StocksTrendingAbove10emaForMonth260524.csv"
# input_file = "../data/sample_screener_name/2024.06.08.csv"
# input_file = "../data/all-emas-in-all-candles-trending_22_12_2024.csv"


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


def get_appearance_count(stocks_data,sorted_date_details, index):
    stocks_count_details = {}
    for stock in stocks_data:
        stocks_count = len(stocks_data[stock])

        for date_detail in sorted_date_details[-index:]:
            if stock in date_detail[1]:
                # print(f'stock found {index-1} days ago : {stock}')
                stocks_count -= 1
        stocks_count_details[stock] = stocks_count
    # print('stocks_count_details :', stocks_count_details)
    return stocks_count_details


def get_new_stocks(count_data, date_data, index):
    new_stocks = list()
    for stock in count_data:
        if (count_data[stock] == 1 and stock in date_data[-index][1]):
            new_stocks.append(stock)
    return new_stocks, date_data[-index][0]


def sort_based_on_appearance_count(data, sorted_dates , top=10):
    high_trening_stocks = {}
    sorted_dict = dict(
        sorted(data.items(), key=lambda item: len(item[1]), reverse=True))
    high_appearance_stocks = {k: len(v) for k, v in
            dict(islice(sorted_dict.items(),
                        top)
                 ).items()
            }
    for stock,count in high_appearance_stocks.items():
        if stock in sorted_dates[-1][1]:
            high_trening_stocks[stock] = count
    return high_trening_stocks



def create_urls(stocks):
    if isinstance(stocks, list):
        return construct_urls(stocks)
    elif isinstance(stocks, dict):
        return construct_urls(stocks.keys())


def construct_urls(stocks):
    urls = list()
    for stock in stocks:
        urls.append(f"https://chartink.com/stocks/{stock.lower()}.html")
    return urls

def input_args():
    parser = argparse.ArgumentParser('Provide inputs for screener data')
    parser.add_argument('--input-csvs-file',
                        help='Input csvs files')
    parser.add_argument('--input-file',
                        help='Input screener file')
    parser.add_argument('--history-days', type=int,
                        default=50)
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
        sorted_date_details = sorted(date_details.items(),
                                     key=lambda x:datetime.strptime(x[0],
                                     '%d-%m-%Y') )
        # ic(stocks_data)
        # ic(sorted_date_details)
        # count_details = get_appearance_count(stocks_data)
        # print('count_details :', count_details)
        for index in range(1, history_days):
            count_details = get_appearance_count(stocks_data,
                                                 sorted_date_details,
                                                 index)
            new_stocks, date = get_new_stocks(count_details, sorted_date_details, index)
            print(f'Newly found stocks {index} days ago on {date}: {new_stocks}')
            for url in create_urls(new_stocks):
                print(f'\t{url}')

        # Sort more trending stocks
        # TODO :Get value of top from user, currently 10
        high_trening_stocks = sort_based_on_appearance_count(stocks_data,
                                                             sorted_date_details,
                                                             top=100)
        print('\nhigh_trening_stocks :', high_trening_stocks)
        for url in create_urls(high_trening_stocks):
            # print(f'\t{url}')
            pass
