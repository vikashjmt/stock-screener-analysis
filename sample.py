import yfinance as yf
#HDFCBANK
msft = yf.Ticker("MSFT")

# get stock info
#print(msft.info)

# get historical market data
hist = msft.history(period="5d")

print(type(hist))
print("History:\n",hist)
