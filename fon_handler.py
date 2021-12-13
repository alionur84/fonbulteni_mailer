import requests
from bs4 import BeautifulSoup
import datetime
import pytz

url = 'https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod='

class Fon:
    def __init__(self, code):
        #self.name = get_name_price(code)[0]
        self.code = code
        #self.price = get_name_price(code)[1]
        #self.daily_change = get_name_price(code)[2]
        #self.time = get_time()

    def get_name(self):
        fon_kod = self.code
        page = requests.get(url + fon_kod)
        soup = BeautifulSoup(page.content, 'html.parser')
        invest_name = soup.find('span', attrs={"id": "MainContent_FormViewMainIndicators_LabelFund"})
        return invest_name.text

    def get_price(self):
        fon_kod = self.code
        page = requests.get(url + fon_kod)
        soup = BeautifulSoup(page.content, 'html.parser')
        top_list = soup.find("ul", class_='top-list')
        price = top_list.find_next("span")
        return price.text

    def daily_change(self):
        fon_kod = self.code
        page = requests.get(url + fon_kod)
        soup = BeautifulSoup(page.content, 'html.parser')
        top_list = soup.find("ul", class_='top-list')
        price = top_list.find_all('span')
        return price[1].text

    def get_name_price(self):
        fon_kod = self.code
        page = requests.get(url + fon_kod)
        soup = BeautifulSoup(page.content, 'html.parser')
        invest_name = soup.find('span', attrs={"id": "MainContent_FormViewMainIndicators_LabelFund"})
        invest_price = soup.find('ul', class_='top-list')
        invest_price = invest_price.find_next("span", class_=None)
        invest_daily = invest_price.find_next("span", class_=None)
        invest_price = invest_price.text
        invest_price = invest_price.replace(",", ".")
        return invest_name.text, float(invest_price), invest_daily.text

    def get_time(self):
        dt_now = datetime.datetime.now(tz=pytz.UTC)
        t_time = dt_now.astimezone(pytz.timezone('Europe/Istanbul'))
        return t_time

