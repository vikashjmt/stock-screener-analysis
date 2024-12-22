# Tool to get analysis on the screener (Chartink)

## Usage

```python3
python3 getDataFromScreener.py -h
usage: Provide inputs for screener data [-h] [--input-file INPUT_FILE] [--history-days HISTORY_DAYS]

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        Input screener file
  --history-days HISTORY_DAYS

```

## Sample Output
```python3
python3 getDataFromScreener.py --input-file ../data/all-emas-in-all-candles-trending_22_12_2024.csv --history-days 10
Newly found stocks 1 days ago on 20-12-2024: []
Newly found stocks 2 days ago on 19-12-2024: []
Newly found stocks 3 days ago on 18-12-2024: []
Newly found stocks 4 days ago on 17-12-2024: ['DYCL']
        https://chartink.com/stocks/dycl.html
Newly found stocks 5 days ago on 16-12-2024: []
Newly found stocks 6 days ago on 13-12-2024: ['RAMASTEEL']
        https://chartink.com/stocks/ramasteel.html
Newly found stocks 7 days ago on 12-12-2024: []
Newly found stocks 8 days ago on 11-12-2024: []
Newly found stocks 9 days ago on 10-12-2024: ['ORIENTTECH', 'WAAREEENER', 'NTPCGREEN', 'EIEL', 'BAJAJHCARE', 'HPL']
        https://chartink.com/stocks/orienttech.html
        https://chartink.com/stocks/waareeener.html
        https://chartink.com/stocks/ntpcgreen.html
        https://chartink.com/stocks/eiel.html
        https://chartink.com/stocks/bajajhcare.html
        https://chartink.com/stocks/hpl.html

high_trening_stocks : {'GOKULAGRO': 119, 'PGEL': 111, 'CIGNITITEC': 110, 'NAUKRI': 108, 'DIXON': 106, 'DEEPINDS': 104, 'KAYNES': 103, 'PERSISTENT': 100, '360ONE': 98, 'GRWRHITECH': 97, 'EIDPARRY': 96, 'ANANTRAJ': 94, 'WEALTH': 93, 'PGIL': 93, 'BHARTIHEXA': 91, 'COROMANDEL': 90, 'OBEROIRLTY': 89, 'PDMJEPAPER': 89, 'KITEX': 88, 'COFORGE': 88, 'ZENTEC': 87, 'TORNTPHARM': 85, 'INDHOTEL': 85, 'UNITDSPR': 84, 'JLHL': 84, 'ZAGGLE': 83, 'NSIL': 83, 'HCG': 83, 'SHAKTIPUMP': 82, 'WELENT': 82, 'RADICO': 82, 'KFINTECH': 81}
```
