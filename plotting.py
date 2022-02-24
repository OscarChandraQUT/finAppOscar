# import relevant libraries
import matplotlib
from msilib.schema import TextStyle
from matplotlib.pyplot import tight_layout
import pandas as pd
import mplfinance as mpf
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

file = 'BTC-USD.csv'
data = pd.read_csv(file)

#convert date column to datetime column
data.Date = pd.to_datetime(data.Date)
#set date as index column
data = data.set_index('Date')

#mpf.plot(data, type = 'line', volume = True)
mpf.plot(data['2021-03': '2021-08'], figratio = (20,12), type= 'candle', title = 'Bitcoin Price 2021/22',
    mav = (20), volume = True, 
    tight_layout = True, style = 'yahoo')

#dont forget to reformat 'prettify'
#print(data)