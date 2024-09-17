#!/usr/bin/env python3

import yfinance as yf
import argparse
import time


def find_max_volume_days(num=2):
    volume_data = data_in_dict['Volume']
    sorted_vol_data = {k: v for k, v in sorted(volume_data.items(), key=lambda item: item[1],reverse=True)}
    #print('volume_data:',sorted_vol_data)
    return list(sorted_vol_data.items())[:num]

def find_max_vol_days_price():
    max_volume_days_price = list()
    price_data = data_in_dict['High']
    count = 0
    #print('price data:\n',price_data)
    for each in max_volume_days:
        count += 1
        data = [ (val,_) for val,_ in price_data.items() if str(each[0]) in str(val)]
        max_vol_price = data[0]
        print(f'max{count} price: {max_vol_price}')
        if count == 1:
            max1 = max_vol_price[-1]
            #print(f'max{count} price: {max1}')
        elif count == 2:
            max2 = max_vol_price[-1]
            #print(f'max{count} price: {max2}')
        else:
            print('Case not handled yet')
    return max1,max2



def get_current_price():
    price = list(data_in_dict['Close'].values())[-1]
    print('\nThe last traded price is:',price)
    print()
    return price

def get_last_day_price():
    ld_price = list(data_in_dict['Close'].values())[-2]
    print("\nThe yesterday closing price is:",ld_price)
    print()
    return ld_price

def find_crucial_price(max1 ,max2, current):
    """Find the crucial price for a given stock 
       based on highest volume high price
    """
    crucial_price = 0
    if max1 < max2:
        if current < max1:
            crucial_price = max1
        else:
            #crucial_price = max2
            crucial_price = max1
    else:
        if current < max2:
            #crucial_price = max2
            crucial_price = max1
        else:
            crucial_price = max1
    return crucial_price

def evaluate_crucial_price(crucial_price,current,last_day_price):
    """ Evaluation between current price and critical price"""
    percent_change = ((current - last_day_price )/last_day_price*100)
    print("The percent change is ",percent_change)
    percent_far = ((current - crucial_price) / crucial_price) * 100.0
    print(f"The stock {stock_name} is {percent_far} % far from critical price")

    if (percent_far < 6 and percent_far >= 0 ):
        print(f"The stock {stock_name} looks good for investment\n")
    elif (percent_far > -3 and percent_far <= 0 and percent_change >=0.4):
        print(f"The stock {stock_name} looks good for investment\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock-list", nargs="+", default=["HDFCBANK.NS","TCS.NS"])
    parse_value =parser.parse_args()
    value = parse_value.stock_list
    print('value:',value)
    for each in value:
        stock_name = each
        print("----------------------------------------------------------------------------------")
        print("\n\nStock name: ",stock_name)
        try:
            stock_data = yf.Ticker(stock_name)
            hist = stock_data.history(period="250d")
            data_in_dict = hist.to_dict()
            max_volume_days = find_max_volume_days(num=2)
            #print("max volume days",max_volume_days)
            max1,max2 = find_max_vol_days_price()
            current= get_current_price()
            last_day_price = get_last_day_price()
            print(f'max1 and max2 price are {max1} and {max2}')
            crucial_price = find_crucial_price(max1,max2,current)
            print(f"The crucial price for the stock is {crucial_price}")
            evaluate_crucial_price(crucial_price,current,last_day_price)
            time.sleep(6)
        except Exception as e:
            print('Issue occured:\n',e)

