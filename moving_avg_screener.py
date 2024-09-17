import json
import yfinance as yf
import requests_cache
import pandas as pd
import pandas_ta as ta
# import talib
from icecream import ic
from send_mail import send_mail
"""
# Calculate the EMA with a period of 10 days and a weighting factor of 0.0001
# df['ema'] = df['close'].ewm(span=10).mean()
df['ema10'] = ta.ema(df['close'], length=10)
# print(df)
# df['ema10_talib'] = talib.EMA(df['close'], timeperiod=10)
print('10 ema :', df)
"""
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'vicky-program/1.0'
user_data = {}
def get_diff_from_close(close, ema):
    return f"{round(((close-ema)/ema)*100,2)} %"


def get_price_for(input_date):
    for date, price in items:
        if (mydate := date.date().strftime("%Y-%m-%d")) == input_date:
            return price
    else:
        ic(f'Seems Market Holiday on the input day {input_date}')


moving_avgs = [10, 21, 50, 150, 200]
moving_avg_values = {}
df = pd.DataFrame()
stocks_list = ["^NSEI","NIFTY_MIDCAP_100.NS","^NSEBANK","CHEMCON.NS","DCAL.NS"]  # TODO : Get this from watchlist
#stocks_list = ["^NSEI"]
tickers = yf.Tickers(' '.join(stock for stock in stocks_list), session=session)

for Stock_number, stock_name in enumerate(stocks_list):
    ic.configureOutput('')
    print()
    ic(Stock_number)
    ic(stock_name)
    # stock = yf.Ticker(stock_name, session=session)
    stock = tickers.tickers.get(stock_name)

    # get stock info
    # print(stock.info)

    # get historical market data
    data = stock.history(period="1y")
    data_dict = data.to_dict()
    df['close'] = list(data_dict.get('Close').values())[-200:]
    items = list(data_dict.get('Close').items())[-200:]
    for moving_avg in moving_avgs:
        # df['close'] = list(data_dict.get('Close').values())[-moving_avg:]
        df[f"ema{moving_avg}"] = ta.ema(df['close'], length=moving_avg)
    day_close = df.iat[199, 0]
    ic.configureOutput(prefix='\t')
    ic(day_close)
    for index, value in enumerate(moving_avgs):
        ema_val = df.iat[199, index+1]
        diff_val = get_diff_from_close(day_close, ema_val)
        moving_avg_values[value] = [diff_val, round(ema_val, 2)]
    ic(moving_avg_values)

    # Calculate change% from given date
    # assume given date is 2024-03-29
    input_date = "2024-03-28"
    input_date_price = get_price_for(input_date)
    ic(input_date_price)
    change_percent_since = get_diff_from_close(day_close, input_date_price)
    ic(change_percent_since)
    
    #Provide processed data in a dictionary
    user_data[Stock_number] = {'stock_name': stock_name,
            'day_close':day_close,
            'moving_avg_values': moving_avg_values,
            'input_date_price': input_date_price,
            'change_percent_since': change_percent_since
            }

with open('stock_details.json', 'w') as fd:
    json.dump(user_data, fd, indent=4)
# send_mail(attachments=['stock_details.json'])
