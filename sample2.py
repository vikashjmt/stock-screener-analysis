import yfinance as yf
import pandas as pd
AMD = yf.Ticker("amd")

AMD_info = AMD.info
AMD_info['volume']

AMD__share_price_data = AMD.history(period="max")
AMD__share_price_data.loc[AMD__share_price_data['Volume'] == AMD__share_price_data['Volume'].max()]
print(AMD__share_price_data.loc[AMD__share_price_data['Volume'])

