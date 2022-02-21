# import relevant libraries
import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


# function to rip the price and % change off page
def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('fin-streamer')
        texts = [span.get_text() for span in spans]
        #print('texts: ' + str(texts))
    except IndexError:
        texts = []
    return texts

def one_year_est(web_content, class_path): #different function because '1y est' is different tag
    one_year_est = web_content.find_all('div', {'class': class_path})
    try:
        infos = one_year_est[0].find_all('td')
        texts = [info.get_text() for info in infos]
        #print(texts)
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):  # get info from url
    url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(
            web_content, "D(ib) Va(m) Maw(65%) Ov(h)")  # div class containing price and % change in 'fin-streamer' tag
        if texts != []:
            price, change, percent = texts[0], texts[1], texts[2]
        else:
            price, change, percent = ['empty'], ['empty'], ['percent']
        #finding volume
        texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)') #class containing volume
        if texts !=[]:
            volume = texts[0]
        else:
            volume = []
        #find one year target
        texts = one_year_est(web_content, 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)') #class containing one year target estimate
        if texts !=[]:
            for count, target in enumerate(texts):
                if target == '1y Target Est': #find relevant 'td' tag
                    one_year_target = texts[count+1] # i want the value after above tag
            #print(one_year_target)
        else:
            one_year_target = []
        #print(texts)
        
        
    except ConnectionError:
        price, change, volume = [], [], []
    return price, change, percent, volume, one_year_target


Stock = ['AAPL']
print(real_time_price('AAPL'))