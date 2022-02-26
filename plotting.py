# import relevant libraries
from msilib.schema import TextStyle
from matplotlib.pyplot import tight_layout
import pandas as pd
import mplfinance as mpf
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

file = 'BTC-USD.csv'
data = pd.read_csv(file)

# convert date column to datetime column
data.Date = pd.to_datetime(data.Date)
# set date as index column
data = data.set_index('Date')

mpf.plot(data['2021-03': '2021-08'], ylabel='US Dollars', ylabel_lower='Volume', figratio=(20, 12), type='candle', title='Bitcoin Price During 2021/22',
         mav=(20), volume=True,
         tight_layout=False, style='yahoo')
