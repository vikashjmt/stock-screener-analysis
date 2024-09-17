import csv
from itertools import islice

# input_file = "data/StocksTrendingAbove10emaForMonth260524.csv"
# input_file = "../data/sample_screener_name/2024.06.08.csv"
input_file = "../data/all-emas-in-all-candles-trending_17_09_2024.csv"

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

def get_appearance_count(stocks_data):
    stocks_count_details = {}
    for stock in stocks_data:
        stocks_count_details[stock] = len(stocks_data[stock])
    # print('stocks_count_details :', stocks_count_details)
    return stocks_count_details

def get_new_stocks(count_data, date_data):
    new_stocks = list()
    for stock in count_data:
        if (count_data[stock] == 1 and stock in list(date_data.values())[-1]):
            new_stocks.append(stock)
    return new_stocks

def sort_based_on_appearance_count(data, top=10):
    sorted_dict = dict(sorted(data.items(), key=lambda item:len(item[1]), reverse=True))
    return { k : len(v) for k,v in 
             dict(islice(sorted_dict.items(),
                  top)
                  ).items()
           }

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


if __name__ == "__main__":
    stocks_data, date_details = get_all_stock_details(input_file)
    #print('Date details:', date_details)
    # print('stocks_data :', stocks_data)
    count_details = get_appearance_count(stocks_data)
    # print('count_details :', count_details)
    new_stocks = get_new_stocks(count_details, date_details)
    print('Newly found stocks :', new_stocks)
    for url in create_urls(new_stocks):
        print(f'\t{url}')

    # Sort more trending stocks
    # TODO :Get value of top from user, currently 10
    high_trening_stocks = sort_based_on_appearance_count(stocks_data, top=20)
    print('\nhigh_trening_stocks :', high_trening_stocks)
    for url in create_urls(high_trening_stocks):
        print(f'\t{url}')
