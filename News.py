import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from datetime import date

class get_News:
    def __init__(self):
        self.stock = []
        self.news = []

    def list_set(self):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info where `Index` == 'SET100'"
        stock = pd.read_sql(query,conn)
        stock = list(stock['Ticker'])
        for i in stock:
            temp = i.split('.')
            self.stock.append(temp[0])
        return self.stock

    def save_data_news(self, data):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        # save the data to the database
        data.to_sql('stock_news',con=conn,if_exists='append',index=False)
            

    def load_data_news(self, date, title, url, ticker):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        cur = conn.cursor()
        query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?" 
        cur.execute(query, (date, title, url, ticker))
        self.news = cur.fetchall()
        return self.news

    def find_link(self, link):
        all_link = []
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'lxml')
        data = soup.find_all(class_="tie-col-md-11 tie-col-sm-10 tie-col-xs-10")
        
        if data == []:
            return False

        for i in data:
            href = i.find('a').get('href')
            all_link.append(href)
        return all_link

    def scrap_news_SET(self, link ,stock):
        all_link = self.find_link(link)

        for i in all_link:
            try:
                url = i
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'lxml')
                get_url = response.url
                title = soup.find(class_="post-title entry-title")
                date = soup.find(class_="date meta-item tie-icon")
                body = soup.find(class_="entry-content entry clearfix")
                tag = soup.find_all(rel="tag")

                date = date.text.split("/")
                date.reverse()
                if int(date[0]) < 2019:
                    return False
                date = "-".join(date)
                date_format = "%Y-%m-%d"
                date_obj = datetime.strptime(date, date_format)

                body = body.text.split("\n")
                body = " ".join(body)

                for ticker in tag:
                    if ticker.text in stock:
                        news =  self.load_data_news(date_obj, title.text, get_url, ticker.text)
                        print(news)
                        if news != []:
                                return False
                        else:
                            ticker = ticker.text + '.BK'
                            df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title.text], 'Link':[get_url], 'Body':[body], 'Ticker':[ticker]})
                            print(df)
                            self.save_data_news(df)              
            except:
                pass
        return True

    def next_page_scrap(self, stock):
        num = 1
        case = True
        while case == True:
            num += 1
            run = self.scrap_news_SET('https://www.kaohoon.com/latest-news/page/'+str(num), stock)
            if run == False:
                print('stop')
                return 'Stop'
        return True
            
    def News_SET100(self):
        self.stock = self.list_set()
        work = True
        while work == True:
            try:
                self.scrap_news_SET('https://www.kaohoon.com/latest-news', self.stock)
                re = self.next_page_scrap(self.stock)
                if re == 'Stop':
                    work = False
            except Exception as e: 
                print(e)
        return True