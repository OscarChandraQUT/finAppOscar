# import relevant libraries
from dataclasses import replace
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
        texts[2] = texts[2].replace('(', '') #cleaning up percentage data
        texts[2] = texts[2].replace(')', '')
        #print(texts[2])
        #print(texts)
    except IndexError:
        texts = []
    return texts

def find_vol(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('fin-streamer')
        texts = [span.get_text() for span in spans]
        #print(texts)
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
        texts = find_vol(web_content, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)') #class containing volume
        if texts !=[]:
            volume = texts[0]
            #print('volume: ' + volume) #<<<
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

 
Stock = ['AAPL', 'GOOG', 'TSLA', 'FB']
#print(real_time_price('AAPL')) # for debug part 1

#storing to CSV file
while(True):
    data = []
    col = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    for stock_code in Stock:
        price, change, percent, volume, one_year_target = real_time_price(stock_code)
        data.append(price)
        data.extend([change])
        data.extend([percent])
        data.extend([str(volume)])
        data.extend([one_year_target])
    
    col = [time_stamp]
    col.extend(data)
    df = pd.DataFrame(col)
    df = df.T
    df.to_csv(str(time_stamp[0:11]) + 'stock data.csv', mode = 'a', header = False)
    print(col)

    