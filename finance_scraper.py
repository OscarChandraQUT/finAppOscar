# import relevant libraries
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


# function to rip the price and % change off page
def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts


def real_time_price(stock_code):  # get info from url
    url = 'https://coinmarketcap.com/currencies/' + stock_code + '/'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(
            web_content, "sc-16r8icm-0 kjciSH priceTitle")  # div class containing price and % change in span
        if texts != []:
            price, change = texts[0], texts[1]
        else:
            price, change = ['empty'], ['empty']
    except ConnectionError:
        price, change = [], []
    return price, change


Stock = ['ethereum']  # variable of stock to search
print(real_time_price('ethereum'))
