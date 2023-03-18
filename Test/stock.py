import plotly.express as px
import pandas as pd

import numpy as np
import pandas as pd
import plotly
from plotly.subplots import make_subplots

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
import sqlite3
import datetime as dt
from datetime import date
from datetime import datetime
import dateutil.relativedelta

import requests
from bs4 import BeautifulSoup

from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

import time

from selenium import webdriver
from selenium.webdriver.common.by import By 


class ML_stock:
    def __init__(self):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.stock = []
        self.news = []

    def getLastDate(self,period,ticker):
        conn = sqlite3.connect("stock.sqlite")
        # Query last element of stock in database
        if period == 'Hour':query = "SELECT * FROM stock_table_hr WHERE `ticker` = '%s'" % ticker
        elif period == 'Day':query = "SELECT * FROM stock_table_d WHERE `ticker` = '%s'" % ticker
        elif period == 'Month':query = "SELECT * FROM stock_table_mo WHERE `ticker` = '%s'" % ticker
        self.r_df = pd.read_sql(query, conn)
        if self.r_df.tail(1).Datetime.to_string().split() == []:
            return False
        # Cut data to get only datatime
        last = self.r_df.tail(1).Datetime.to_string().split()
        try:
            self.LastDate = last[1].split()[0].split('-')
        except:
            return False
        return self.LastDate

    def getDiffDay(self):
        # Get datetime for now
        x = dt.datetime.now()
        if self.LastDate == False:
            return False
        count = 0
        DayM = 0
        DayMo365 = {'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
        DiffMo = int(x.month) - int(self.LastDate[1])
        DiffYe = int(x.year) - int(self.LastDate[0])
        # Get differend day for dowload stock
        if DiffYe == 0:
            if DiffMo == 0:
                DiffDay = int(x.day) - int(self.LastDate[2])
                if DiffDay != 0:
                    pass
            elif DiffMo != 0 :
                for u in range(DiffMo):
                    DayM = DayM + DayMo365[str(int(self.LastDate[1])+count)]
                    count += 1
                DiffDay = DayM - int(self.LastDate[2]) + int(x.day)
        elif DiffYe != 0:
            dayly = 0
            dayn = 0
            for j in range(1,int(self.LastDate[1])):
                dayly = dayly + DayMo365[str(j)]
            for i in range(1,int(x.month)):
                dayn = dayn + DayMo365[str(i)]
            DiffDay = (365*DiffYe) - dayly + dayn - int(self.LastDate[2]) + int(x.day)   
        self.DiffDay = DiffDay
        return self.DiffDay
        
    def check_stock(self,ticker):
        conn = sqlite3.connect("stock.sqlite")
        down = 0
        query = "SELECT `Index` FROM stock_info WHERE `ticker` = '%s'" % ticker
        for_ind = pd.read_sql(query, conn)
        ok = self.r_df.tail(1).Datetime.to_string().split()[2]
        #for get extra time in database
        if for_ind['Index'].values == 'NASDAQ':
            self.DiffDay = str(self.DiffDay+2)+'d'
            if ok == '09:30:00':down = 0
            elif ok == '10:30:00':down = 1
            elif ok == '11:30:00':down = 2
            elif ok == '12:30:00':down = 3
            elif ok == '13:30:00':down = 4
            elif ok == '14:30:00':down = 5
            elif ok == '15:30:00':down = 6
        elif for_ind['Index'].values == 'SET100':
            self.DiffDay = str(self.DiffDay+1)+'d'
            if ok == '10:00:00':down = 0
            elif ok == '11:00:00':down = 1
            elif ok == '12:00:00':down = 2
            elif ok == '14:00:00':down = 3
            elif ok == '15:00:00':down = 4
            elif ok == '16:00:00':down = 5
        elif for_ind['Index'].values == 'CRYPTO100':
            self.DiffDay = str(self.DiffDay+2)+'d'
            if ok == '00:00:00':down = 0
            elif ok == '01:00:00':down = 1
            elif ok == '02:00:00':down = 2
            elif ok == '03:00:00':down = 3
            elif ok == '04:00:00':down = 4
            elif ok == '05:00:00':down = 5
            elif ok == '06:00:00':down = 6
            elif ok == '07:00:00':down = 7
            elif ok == '08:00:00':down = 8
            elif ok == '09:00:00':down = 9
            elif ok == '10:00:00':down = 10
            elif ok == '11:00:00':down = 11
            elif ok == '12:00:00':down = 12
            elif ok == '13:00:00':down = 13
            elif ok == '14:00:00':down = 14
            elif ok == '15:00:00':down = 15
            elif ok == '16:00:00':down = 16
            elif ok == '17:00:00':down = 17
            elif ok == '18:00:00':down = 18
            elif ok == '19:00:00':down = 19
            elif ok == '20:00:00':down = 20
            elif ok == '21:00:00':down = 21
            elif ok == '22:00:00':down = 22
            elif ok == '23:00:00':down = 23
        self.down = down
        return self.down
    
    def update(self,period,ticker):
        count = 0
        conn = sqlite3.connect("stock.sqlite")
        # Select period to download
        if period == 'Hour':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1h',progress=False)
        elif period == 'Day':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1d',progress=False)
        elif period == 'Month':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1mo',progress=False)
        # Get number of extra stock
        for i in data.index.day:
            if data.index.year[count] == int(self.LastDate[0]):
                if data.index.month[count] == int(self.LastDate[1]):
                    if period == 'Month':
                        if i == int(self.LastDate[2])+1 or i == int(self.LastDate[2])+2 or i == int(self.LastDate[2])+3 or i == int(self.LastDate[2]):
                            if str(data.index.values[0]).split('T')[0] == self.r_df.tail(1)['Datetime'].values[0].split(' ')[0]:
                                count += 1
                            break
                    else:
                        if i == int(self.LastDate[2])+1 or i == int(self.LastDate[2])+2 or i == int(self.LastDate[2])+3 or i == int(self.LastDate[2]):
                            count += 1
                            break
            count += 1
        # Cut extra stock off
        if count != len(data):
            count = count + self.down
        data['ticker'] = ticker
        data = data.iloc[count:,:]
        data.index.names = ['Datetime']
        # Select period to download and Save to sqlite
        if period == 'Hour':data.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        elif period == 'Day':data.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        elif period == 'Month':data.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)
        return data
    
    def savetoDB(self,period,data):
        conn = sqlite3.connect("stock.sqlite")
        if period == 'Hour':data.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        elif period == 'Day':data.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        elif period == 'Month':data.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)

    def getAllticker(self):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info"
        r_df = pd.read_sql(query,conn)
        self.list_db = r_df['Ticker'].values.tolist()
        return self.list_db

    def download_ticker(self,period,ticker):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        try:
            # Select period to download
            if period == 'Hour':
                data = yf.download(tickers=ticker, period='2y', interval='1h')
            elif period == 'Day':
                data = yf.download(tickers=ticker, period='max', interval='1d')
            elif period == 'Month':
                data = yf.download(tickers=ticker, period='max', interval='1mo')
            else:
                data = None
            # Save to sqlite3
            data.to_sql('stock_table',con=conn,if_exists='append',index=True)
            # return data to ploting graph
            return data
        except:
            return False

    #return all stock    
    def stock_name(self):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info"
        r_df = pd.read_sql(query,conn)
        list_db = r_df['Ticker'].values.tolist()
        return list_db

    #return all stock in SET100    
    def list_set(self):
        self.stock = []
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info where `Index` == 'SET100'"
        stock = pd.read_sql(query,conn)
        stock = list(stock['Ticker'])
        for i in stock:
            temp = i.split('.')
            self.stock.append(temp[0])
        return self.stock
    
    #return all stock in NASDAQ
    def list_nasdaq(self):
        self.stock = []
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info where `Index` == 'NASDAQ'"
        stock = pd.read_sql(query,conn)
        self.stock = list(stock['Ticker'])
        return self.stock
    
    #return all Crypto100 
    def list_crypto(self):
        self.stock = []
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query = "select Ticker from stock_info where `Index` == 'CRYPTO100'"
        stock = pd.read_sql(query,conn)
        stock = list(stock['Ticker'])
        for i in stock:
            temp = i.split('-')
            self.stock.append(temp[0])
        return self.stock

    #save news into database
    def save_data_news(self, data):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        # save the data to the database
        data.to_sql('stock_news',con=conn,if_exists='append',index=False)
            
    #load news from database 
    def load_data_news(self, date, title, url, ticker):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        cur = conn.cursor()
        query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?" 
        cur.execute(query, (date, title, url, ticker))
        self.news = cur.fetchall()
        return self.news

    #find all link news in website
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

    #scrap news from website
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
                        ticker = ticker.text + '.BK'
                        self.news =  self.load_data_news(date_obj, title.text, get_url, ticker)
                        print(self.news)
                        if self.news != []:
                            return False
                        else:
                            df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title.text], 'Link':[get_url], 'Body':[body], 'Ticker':[ticker]})
                            print(df)
                            self.save_data_news(df)                
            except:
                pass
        return True 
    
    #find next page
    def next_page_scrap(self, stock):
        try:
            num = 1
            case = True
            while case == True:
                num += 1
                run = self.scrap_news_SET('https://www.kaohoon.com/latest-news/page/'+str(num), stock)
                if run == False:
                    return 'Stop'
        except:
            return 'Error'
        
    #main scraping function        
    def News_SET100(self):
        self.stock = self.list_set()
        work = True
        while work == True:
            try:
                re = self.scrap_news_SET('https://www.kaohoon.com/latest-news', self.stock)
                re = self.next_page_scrap(self.stock)
                if re == 'Stop' or re == False:
                    work = False
            except Exception as e: 
                print(e)
        return True
    
        #scrap news from API
    def news_one_Nasdaq(self,ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        try:
            if ticker in self.list_nasdaq():
                url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='+ ticker +'&limit=200&apikey=8X8QE27D001F3TV'
                r = requests.get(url)
                data = r.json()
                round = int(data['items'])
                for j in range(round):
                    print(j)
                    title = data['feed'][j]['title']
                    date = data['feed'][j]['time_published']
                    get_url = data['feed'][j]['url']
                    body = data['feed'][j]['summary']

                    date = date.split("T")
                    date = date[0]
                    year = date[:4]
                    mo = date[4:6]
                    day = date[6:]

                    date = [year,mo,day]
                    date = "-".join(date)
                    date_format = "%Y-%m-%d"
                    date_obj = datetime.strptime(date, date_format)

                    query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?"
                    cur.execute(query, (date_obj, title, get_url, ticker))
                    news = cur.fetchall()
                    print(news)
                    if news != []:
                        break
                    else:
                        df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title], 'Link':[get_url], 'Body':[body], 'Ticker':[ticker]})
                        print(df)
                        self.save_data_news(df)
                return True
            else:
                return False
        except:
            return False
    
    #scrap news from API
    #fix integer is 0
    def news_Nasdaq(self,interger):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        try:
            for i in self.stock[interger:]:
                ind = self.stock.index(i)
                url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='+ i +'&limit=200&apikey=8X8QE27D001F3TV'
                r = requests.get(url)
                data = r.json()
                round = int(data['items'])
                for j in range(round):
                    print(j)
                    title = data['feed'][j]['title']
                    date = data['feed'][j]['time_published']
                    get_url = data['feed'][j]['url']
                    body = data['feed'][j]['summary']

                    date = date.split("T")
                    date = date[0]
                    year = date[:4]
                    mo = date[4:6]
                    day = date[6:]

                    date = [year,mo,day]
                    date = "-".join(date)
                    date_format = "%Y-%m-%d"
                    date_obj = datetime.strptime(date, date_format)

                    query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?"
                    cur.execute(query, (date_obj, title, get_url, i))
                    news = cur.fetchall()
                    print(news)
                    if news != []:
                        break
                    else:
                        df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title], 'Link':[get_url], 'Body':[body], 'Ticker':[i]})
                        print(df)
                        self.save_data_news(df)
            return True
        except: 
            self.news_Nasdaq(ind)

    #scrap news from API
    def news_one_Crypto(self, ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        try:
            if ticker in self.list_crypto():
                # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
                url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&blockchain='+ ticker +'&limit=200&apikey=8X8QE27D001F3TV'
                r = requests.get(url)
                data = r.json()
                round = int(data['items'])
                for j in range(round):
                    print(j)
                    title = data['feed'][j]['title']
                    date = data['feed'][j]['time_published']
                    get_url = data['feed'][j]['url']
                    body = data['feed'][j]['summary']
                    date = date.split("T")
                    date = date[0]
                    year = date[:4]
                    mo = date[4:6]
                    day = date[6:]
                    date = [year,mo,day]
                    date = "-".join(date)
                    date_format = "%Y-%m-%d"
                    date_obj = datetime.strptime(date, date_format)

                    query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?"
                    cur.execute(query, (date_obj, title, get_url, ticker))
                    news = cur.fetchall()
                    print(news)
                    if news != []:
                        break
                    else:
                        df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title], 'Link':[get_url], 'Body':[body], 'Ticker':[ticker]})
                        print(df)
                        self.save_data_news(df)
                return True
            else:
                return False
        
        except:
            return False

    #scrap news from API
    #fix integer is 0
    def news_Crypto(self, interger):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        try:
            for i in self.stock[interger:]:
                print(i)
                ind = self.stock.index(i)
                cryp = i.split('-')
                cryp = cryp[0]
                # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
                url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&blockchain='+ cryp +'&limit=200&apikey=8X8QE27D001F3TV'
                r = requests.get(url)
                data = r.json()
                round = int(data['items'])
                for j in range(round):
                    print(j)
                    title = data['feed'][j]['title']
                    date = data['feed'][j]['time_published']
                    get_url = data['feed'][j]['url']
                    body = data['feed'][j]['summary']
                    date = date.split("T")
                    date = date[0]
                    year = date[:4]
                    mo = date[4:6]
                    day = date[6:]
                    date = [year,mo,day]
                    date = "-".join(date)
                    date_format = "%Y-%m-%d"
                    date_obj = datetime.strptime(date, date_format)

                    query = "SELECT * FROM stock_news WHERE DATETIME = ? AND Title = ? AND Link = ? AND Ticker = ?"
                    cur.execute(query, (date_obj, title, get_url, i))
                    news = cur.fetchall()
                    print(news)
                    if news != []:
                        break
                    else:
                        df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title], 'Link':[get_url], 'Body':[body], 'Ticker':[i]})
                        print(df)
                        self.save_data_news(df)
            return True
        except : 
            self.news_Crypto(ind)

    def get_news_content(self):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        self.content_news = pd.DataFrame()

        for i in self.list_db:
            query2 = "SELECT ticker,body FROM stock_news WHERE `Ticker` = '%s'" % i
            news = pd.read_sql(query2, conn)
            if not(news.empty):
                self.content_news = pd.concat([self.content_news,news],ignore_index=True)
    
    def getcity_and_latlong(self,text):
        # extracting entities.
        place_entity = locationtagger.find_locations(text = text)

        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")
        address = pd.DataFrame({'city': [],'lat':[],'long':[]})

        for i in place_entity.cities:
            getLoc = loc.geocode(i)
            ones_city = pd.DataFrame({'city':[i],'lat':[getLoc.latitude],'long':[getLoc.longitude]})
            # getting all cities
            address = pd.concat([address,ones_city],ignore_index=True)
        return address
    
    def get_latlong_for_all_content(self):
        self.place = pd.DataFrame()
        count = 0
        for i in self.content_news['Body']:
            if count < 1000:
                data = self.getcity_and_latlong()
                self.place = pd.concat([self.place,data],ignore_index=True)
            else:
                break
            count += 1
        return self.place
    
    def get_poppulate_for_city(self):
        self.add = self.place.groupby(self.place.columns.tolist(),as_index=False).size()
        self.add.rename(columns={'size': 'population'}, inplace=True)
        return self.add

    def updateAll(self):
        period = ['Hour','Day','Month']
        Ticker = self.getAllticker()
        self.News_SET100()
        self.list_nasdaq()
        self.news_Nasdaq(0)
        self.list_crypto()
        self.news_Crypto(0)
        for  i in Ticker:
            try:
                for j in period:
                    self.getLastDate(j,i)
                    self.getDiffDay()
                    self.check_stock(i)
                    self.update(j,i)
            except:
                pass
        
            
    def stock_info(self,ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_info where Ticker = '"+ticker+"';",con)
        data = data.drop(columns=['Ticker'])
        return data

    def table_finance(self, ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_financial where Ticker = '"+ticker+"';",con)
        column = data['Year'].values.tolist()
        data = data.transpose()
        data.columns = column
        data = data.drop("Ticker")
        data = data.drop("Year")
        head = data.index.values.tolist()
        data.insert(0, "Financial Information", head, True)
        return data

    def table_quarterly(self, ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_quarter where Ticker = '"+ticker+"';",con)
        data = data.drop(columns=['Ticker'])
        column = data['Quarterly'].values.tolist()
        data = data.transpose()
        data.columns = column
        data = data.drop("Quarterly")
        head = data.index.values.tolist()
        data.insert(0, "Quarterly", head, True)
        return data

    def table_news(self, ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_news where Ticker = '"+ticker+"' order by Datetime desc;",con)
        data = data.drop(columns=['Ticker'])
        return data



    def plot(self, ticker, interval):
        now = dt.datetime.now()
        last_month = now + dateutil.relativedelta.relativedelta(months=-1)
        seven_month = now + dateutil.relativedelta.relativedelta(months=-7)
        ten_year = now + dateutil.relativedelta.relativedelta(years=-10)
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query1 = "SELECT * FROM stock_table_hr WHERE `ticker` == '%s' AND datetime > '%s' AND datetime < '%s'" % (ticker, last_month, now)
        query2 = "SELECT * FROM stock_table_d WHERE `ticker` == '%s' AND datetime > '%s' AND datetime < '%s'" % (ticker, seven_month, now)
        query3 = "SELECT * FROM stock_table_mo WHERE `ticker` == '%s' AND datetime > '%s' AND datetime < '%s'" % (ticker, ten_year, now)
        Hr = pd.read_sql(query1,conn)
        Day = pd.read_sql(query2,conn)
        Mo = pd.read_sql(query3,conn)
        #declare figure
        fig = go.Figure()
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.1, subplot_titles=('OHLC', 'Volume','MACD'), 
                    row_width=[0.2, 0.2, 0.6])

        #Candlestick

        # fig.update_xaxes( rangebreaks=[ dict(values = timegap_hr , dvalue = 3600000)])
        if interval == "Hour":
            Hr['time'] = pd.to_datetime(Hr['Datetime'])
            Hr['MA50'] = Hr['Close'].rolling(window = 50 , min_periods = 0).mean()
            Hr['MA200'] = Hr['Close'].rolling(window = 200 , min_periods = 0).mean()
            Hr['EMA12'] = Hr['Close'].ewm(span=12, adjust=False, min_periods = 0).mean()
            Hr['EMA26'] = Hr['Close'].ewm(span=26, adjust=False, min_periods = 0).mean()
            Hr.set_index(Hr['time'],inplace = True)
            macd = Hr['EMA12'] - Hr['EMA26']
            Hr['Signal'] = 0.0  
            Hr['Signal'] = np.where(Hr['EMA12'] > Hr['EMA26'], 1.0, 0.0)
            # create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
            Hr['Position'] = Hr['Signal'].diff()
            signal = macd.ewm(span=9, adjust=False).mean()
            fig.add_trace(go.Candlestick(x=Hr.Datetime,
                            open=Hr.Open,
                            high=Hr.High,
                            low=Hr.Low,
                            close=Hr.Close, 
                            name = ticker,),row=1, col=1)

            fig.add_trace(go.Scatter(name = 'MA50',x=Hr.Datetime,y=Hr['MA50']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'MA200',x=Hr.Datetime,y=Hr['MA200']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA12',x=Hr.Datetime,y=Hr['EMA12']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA26',x=Hr.Datetime,y=Hr['EMA26']),row=1, col=1)
            fig.add_trace(go.Bar(x=Hr.Datetime, y=Hr.Volume,showlegend=False), row=2, col=1)
            fig.add_trace(go.Bar(name = 'MACD',x=Hr.Datetime,y=signal),row=3, col=1)
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="LightSeaGreen"),name = 'Buy',x=Hr[Hr['Position'] == 1].Datetime,y=Hr['EMA12'][Hr['Position'] == 1]))
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="hotpink"),name = 'Sell',x=Hr[Hr['Position'] == -1].Datetime,y=Hr['EMA12'][Hr['Position'] == -1]))
            
            df_resample_hr = Hr.resample('H').max()
            merged_index_hr  = Hr.index.append(df_resample_hr.index)
            timegap_hr = merged_index_hr[~merged_index_hr.duplicated(keep = False)]
            fig.update_xaxes(rangebreaks=[dict(values=timegap_hr, dvalue=3600000)])
            
        elif interval == "Day":
            Day['time'] = pd.to_datetime(Day['Datetime'])
            Day['MA50'] = Day['Close'].rolling(window = 50 , min_periods = 0).mean()
            Day['MA200'] = Day['Close'].rolling(window = 200 , min_periods = 0).mean()
            Day['EMA12'] = Day['Close'].ewm(span=12, adjust=False, min_periods = 0).mean()
            Day['EMA26'] = Day['Close'].ewm(span=26, adjust=False, min_periods = 0).mean()
            macd = Day['EMA12'] - Day['EMA26']
            Day['Signal'] = 0.0  
            Day['Signal'] = np.where(Day['EMA12'] > Day['EMA26'], 1.0, 0.0)
            # create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
            Day['Position'] = Day['Signal'].diff()
            signal = macd.ewm(span=9, adjust=False).mean()
            Day.set_index(Day['time'],inplace = True)
            fig.add_trace(go.Candlestick(x=Day.Datetime,
                            open=Day.Open,
                            high=Day.High,
                            low=Day.Low,
                            close=Day.Close, 
                            name = ticker,),row=1, col=1)
                            
            fig.add_trace(go.Scatter(name = 'MA50',x=Day.Datetime,y=Day['MA50']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'MA200',x=Day.Datetime,y=Day['MA200']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA12',x=Day.Datetime,y=Day['EMA12']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA26',x=Day.Datetime,y=Day['EMA26']),row=1, col=1)
            fig.add_trace(go.Bar(x=Day.Datetime, y=Day.Volume,showlegend=False), row=2, col=1)
            fig.add_trace(go.Bar(name = 'MACD',x=Day.Datetime,y=signal),row=3, col=1)
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="LightSeaGreen"),name = 'Buy',x=Day[Day['Position'] == 1].Datetime,y=Day['EMA12'][Day['Position'] == 1]))
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="hotpink"),name = 'Sell',x=Day[Day['Position'] == -1].Datetime,y=Day['EMA12'][Day['Position'] == -1]))
        
            df_resample_day = Day.resample('D').max()
            merged_index_day  = Day.index.append(df_resample_day.index)
            timegap_day = merged_index_day[~merged_index_day.duplicated(keep = False)]
            fig.update_xaxes(rangebreaks=[dict(values=timegap_day)])

        elif interval == "Month":
            Mo['time'] = pd.to_datetime(Mo['Datetime'])
            Mo['MA50'] = Mo['Close'].rolling(window = 50 , min_periods = 0).mean()
            Mo['MA200'] = Mo['Close'].rolling(window = 200 , min_periods = 0).mean()
            Mo['EMA12'] = Mo['Close'].ewm(span=12, adjust=False, min_periods = 0).mean()
            Mo['EMA26'] = Mo['Close'].ewm(span=26, adjust=False, min_periods = 0).mean()
            Mo.set_index(Mo['time'],inplace = True)
            macd = Mo['EMA12'] - Mo['EMA26']
            Mo['Signal'] = 0.0  
            Mo['Signal'] = np.where(Mo['EMA12'] > Mo['EMA26'], 1.0, 0.0)
            # create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
            Mo['Position'] = Mo['Signal'].diff()
            signal = macd.ewm(span=9, adjust=False).mean()
            fig.add_trace(go.Candlestick(x=Mo.Datetime,
                            open=Mo.Open,
                            high=Mo.High,
                            low=Mo.Low,
                            close=Mo.Close, 
                            name = ticker,),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'MA50',x=Mo.Datetime,y=Mo['MA50']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'MA200',x=Mo.Datetime,y=Mo['MA200']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA12',x=Mo.Datetime,y=Mo['EMA12']),row=1, col=1)
            fig.add_trace(go.Scatter(name = 'EMA26',x=Mo.Datetime,y=Mo['EMA26']),row=1, col=1)
            fig.add_trace(go.Bar(x=Mo.Datetime, y=Mo.Volume,showlegend=False), row=2, col=1)
            fig.add_trace(go.Bar(name = 'MACD',x=Mo.Datetime,y=signal),row=3, col=1)
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="LightSeaGreen"),name = 'Buy',x=Mo[Mo['Position'] == 1].Datetime,y=Mo['EMA12'][Mo['Position'] == 1]))
            fig.add_trace(go.Scatter(mode="markers",marker=dict(size=10, color="hotpink"),name = 'Sell',x=Mo[Mo['Position'] == -1].Datetime,y=Mo['EMA12'][Mo['Position'] == -1]))
        
        fig.update_xaxes(rangemode="nonnegative")
        fig.update_yaxes(fixedrange=False)

        fig.update_layout(hovermode = "x", plot_bgcolor='#26262e', paper_bgcolor='#272B30',font_color='white')
        fig.update(layout_xaxis_rangeslider_visible=False)
        return fig
    
    def plot_spatial(self, ticker):
        conn = sqlite3.connect("stock.sqlite")
        query = "SELECT city,lat,long FROM stock_city WHERE Ticker = '%s'" % ticker
        address = pd.read_sql(query, conn)
        add = address.groupby(address.columns.tolist(),as_index=False).size()
        add.rename(columns={'size': 'population'}, inplace=True)
        df = add

        fig = px.scatter_geo(df,lat="lat", lon="long", color="population",
                        hover_name="city", size="population",
                        projection="natural earth")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#272B30', font_color='white')
        return fig
    
    def trans_set100(self,df2):
        count = 0
        a = len(df2)
        data_thai = pd.DataFrame()
        for i in range(a):
            try:
                data = pd.DataFrame({'Datetime':[df2.iloc[i]['Datetime']],'Ticker':[df2.iloc[i]['Ticker']],'Body':[tss.google(df2.iloc[i]['Body'])]})
                data_thai = pd.concat([data_thai,data],ignore_index=True)
            except:
                pass
        return data_thai
    
    def download_place(self,ticker):
        conn = sqlite3.connect("stock.sqlite")
        query_index = "SELECT `Index` FROM stock_info WHERE `Ticker` = '%s'" % ticker
        check_index = pd.read_sql(query_index, conn).values.tolist()[0][0]
        query_news = "SELECT Datetime,ticker,body FROM stock_news WHERE `Ticker` == '%s'" % (ticker)
        get_news = pd.read_sql(query_news, conn)
        if check_index == 'SET100':
            eng = self.trans_set100(get_news)
            place = self.get_latlong_for_all_content(eng)
        else:
            place = self.get_latlong_for_all_content(get_news)
        place.to_sql('stock_city',con=conn,if_exists='append',index=False)
        return place
    
    def update_place(self,ticker):
        conn = sqlite3.connect("stock.sqlite")
        query_index = "SELECT `Index` FROM stock_info WHERE `Ticker` = '%s'" % ticker
        check_index = pd.read_sql(query_index, conn).values.tolist()[0][0]
        query_Dplace = "SELECT Datetime FROM stock_city WHERE `Ticker` = '%s'" % ticker
        check_Dplace = pd.read_sql(query_Dplace, conn).sort_values(by=['Datetime'],ascending=False).values.tolist()[0][0]
        query_news = "SELECT Datetime,ticker,body FROM stock_news WHERE datetime > '%s' and `Ticker` == '%s'" % (check_Dplace,ticker)
        get_news = pd.read_sql(query_news, conn)
        if check_index == 'SET100':
            eng = self.trans_set100(get_news)
            place = self.get_latlong_for_all_content(eng)
        else:
            place = self.get_latlong_for_all_content(get_news)
        place.to_sql('stock_city',con=conn,if_exists='append',index=False)
        return place

    def download_info(self,Ticker):
        conn = sqlite3.connect("stock.sqlite")
        all_link = []
        op = webdriver.ChromeOptions()
        op.add_argument('headless') 
        driver = webdriver.Chrome(options=op)
        df2 = pd.DataFrame()
        InsSec = []
        driver.get("https://finance.yahoo.com/quote/%s/profile?p=%s"% (Ticker,Ticker))
        numlink = driver.find_elements(By.XPATH, '//span[@class="Fw(600)"]')
        for i in numlink[:2]:
            InsSec.append(i.text)
        df1 = pd.DataFrame({'Ticker': [Ticker], 'Industry Group': [InsSec[0]], 'Sector': [InsSec[1]], 'Index': ['NASDAQ']})
        df1.to_sql('stock_info',con=conn,if_exists='append',index=False)
        return df1

    def download_stock(self,Ticker):
        conn = sqlite3.connect("stock.sqlite")
        df_h = yf.download(tickers=Ticker, period='2y', interval='1h')
        df_h['Ticker'] = Ticker
        df_d = yf.download(tickers=Ticker, period='max', interval='1d')
        df_d['Ticker'] = Ticker
        df_d.index.names = ['Datetime']
        df_mo = yf.download(tickers=Ticker, period='max', interval='1mo')
        df_mo['Ticker'] = Ticker
        df_mo.index.names = ['Datetime']

        df_h.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        df_d.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        df_mo.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)

    def download_year(self,ticker,save):
        test = []
        test2 = []
        test3 = []
        count = 0
        revenue,YoYR = [],[]

        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect("stock.sqlite")

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
        thf2 = pd.DataFrame()
        query_index = "SELECT `Index` FROM stock_info WHERE `Ticker` = '%s'" % ticker
        check_index = pd.read_sql(query_index, conn).values.tolist()[0][0]
        tickerest = ticker.split('.')[0]
        if check_index == 'SET100':
            driver.get('https://www.tradingview.com/symbols/SET-%s/financials-income-statement/'% tickerest)
        else:
            driver.get('https://www.tradingview.com/symbols/NASDAQ-%s/financials-income-statement/'% tickerest)
        time.sleep(4)
        year = driver.find_element("xpath",'//*[@id="FY"]')
        year.click()
        header = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]')
        raw1 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]')
        raw2 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]')
        raw3 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]')
        raw4 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[5]')
        raw5 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[6]')
        raw6 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[7]')
        raw7 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[8]')
        raw8 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[9]')
        raw9 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[10]')
        raw10 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[11]')
        raw11 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[12]')
        raw12 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[13]')
        raw13 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[14]')
        raw14 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[15]')
        raw15 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[16]')
        raw16 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[17]')
        raw17 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[18]')
        raw18 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]')
        raw19 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[20]')
        raw20 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[21]')
        raw21 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[22]')
        raw22 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[23]')
        raw23 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[24]')
        raw24 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[25]')
        time.sleep(4)
        Allelement = [raw1,raw2,raw3,raw4,raw5,raw6,raw7,raw8,raw9,raw10,
                    raw11,raw12,raw13,raw14,raw15,raw16,raw17,raw18,raw19,raw20,
                    raw21,raw22,raw23,raw24]

        YoY = [''] * len(Allelement)
        Oth = [''] * len(Allelement)
        for element in header:
            test.append(element.text)
        year = test[0].split('\n')[1:-1]
        for e in Allelement:
            revenue = []
            YoYR = []
            test2 = []
            for h in e:
                test2.append(h.text)
            test2 = test2[0].split('\n')
            if (e == raw1) or (e == raw3) or (e == raw5) or (e == raw7) or (e == raw14) or (e == raw18) or (e == raw19) or (e == raw22) or (e == raw23):
                for k in range(len(test2)-1):
                    if k%2 == 0 and k > 0:
                        YoYR.append(test2[k])
                    else:
                        if k > 0 :
                            a = test2[k]
                            revenue.append(a[1:-1])
            else:
                for k in range(len(test2)-2):
                    a = test2[k+1]
                    YoYR.append(None)
                    revenue.append(a[1:-1])

            YoY[count] = (YoYR)
            Oth[count] = (revenue)
            count += 1
        a = range(len(Oth))
        s = '2018'
        for i in range(len(year)):
            if year[i] == s:
                year = year[i:]
                break
        for i in range(len(year)):
            try:
                data = {'Ticker':(ticker),'Total revenue':Oth[0][i],'YoY growth Total revenue':YoY[0][i],
                    'Cost of goods sold':Oth[1][i],
                    'Gross profit':Oth[2][i],'YoY growth Gross profit':YoY[2][i],
                    'Operating expenses (excl. COGS)':Oth[3][i],
                    'Operating income':Oth[4][i],'YoY growth Operating income' : YoY[4][i],
                    'Non-operating income, total':Oth[5][i],
                    'Pretax income':Oth[6][i],'YoY growth Pretax income':YoY[6][i],
                    'Equity in earnings':Oth[7][i],'Taxes':Oth[8][i],
                    'Non-controlling/minority interest':Oth[9][i],'After tax other income/expense':Oth[10][i],
                    'Net income before discontinued operations':Oth[11][i],'Discontinued operations':Oth[12][i],
                    'Net income':Oth[13][i],'YoY growth Net income':YoY[13][i],
                    'Dilution adjustment':Oth[14][i],'Preferred dividends':Oth[15][i],'Diluted net income available to common stockholders':Oth[16][i],
                    'Basic EPS':Oth[17][i],'YoY growth Basic EPS':YoY[17][i],'Diluted EPS':Oth[18][i],'Diluted EPS YoY growth':YoY[18][i],
                    'Average basic shares outstanding':Oth[19][i],'Diluted shares outstanding':Oth[20][i],
                    'EBITDA':Oth[21][i],'YoY growth EBITDA':YoY[21][i],'EBIT':Oth[22][i],'YoY growth EBIT': YoY[22][i],
                    'Total operating expenses':Oth[23][i],'Year':year[i]}
                thf = pd.DataFrame(data,index=[i])
                thf2 = pd.concat([thf2,thf],ignore_index=True)
            except:
                print(i)
                print('error here')
        count = 0
        year = []
        if save == True:
            thf2.to_sql('stock_financial',con=conn,if_exists='append',index=False)
        return thf2

    def download_quarter(self,ticker,save):
        test = []
        test2 = []
        test3 = []
        count = 0
        revenue,YoYR = [],[]

        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect("stock.sqlite")

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
        thf2 = pd.DataFrame()
        query_index = "SELECT `Index` FROM stock_info WHERE `Ticker` = '%s'" % ticker
        check_index = pd.read_sql(query_index, conn).values.tolist()[0][0]
        tickerest = ticker.split('.')[0]
        if check_index == 'SET100':
            driver.get('https://www.tradingview.com/symbols/SET-%s/financials-income-statement/'% tickerest)
        else:
            driver.get('https://www.tradingview.com/symbols/NASDAQ-%s/financials-income-statement/'% tickerest)

        header = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]')
        raw1 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]')
        raw2 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]')
        raw3 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]')
        raw4 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[5]')
        raw5 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[6]')
        raw6 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[7]')
        raw7 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[8]')
        raw8 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[9]')
        raw9 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[10]')
        raw10 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[11]')
        raw11 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[12]')
        raw12 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[13]')
        raw13 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[14]')
        raw14 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[15]')
        raw15 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[16]')
        raw16 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[17]')
        raw17 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[18]')
        raw18 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[19]')
        raw19 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[20]')
        raw20 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[21]')
        raw21 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[22]')
        raw22 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[23]')
        raw23 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[24]')
        raw24 = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div/div[2]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[25]')
        time.sleep(4)
        Allelement = [raw1,raw2,raw3,raw4,raw5,raw6,raw7,raw8,raw9,raw10,
                    raw11,raw12,raw13,raw14,raw15,raw16,raw17,raw18,raw19,raw20,
                    raw21,raw22,raw23,raw24]

        YoY = [''] * len(Allelement)
        Oth = [''] * len(Allelement)
        for element in header:
            test.append(element.text)
        year = test[0].split('\n')[1:-1]
        for e in Allelement:
            test2 = []
            for h in e:
                test2.append(h.text)
            test2 = test2[0].split('\n')
            if (e == raw1) or (e == raw3) or (e == raw5) or (e == raw7) or (e == raw14) or (e == raw18) or (e == raw19) or (e == raw22) or (e == raw23):
                for k in range(len(test2)-3):
                    if k%2 == 0:
                        a = test2[k+2]
                        revenue.append(a[1:-1])
                    else:
                        YoYR.append(test2[k+2])
            else:
                for k in range(len(test2)-2):
                    a = test2[k+1]
                    revenue.append(a[1:-1])
                    YoYR.append(None)

            YoY[count] = (YoYR)
            Oth[count] = (revenue)
            count += 1
            YoYR = []
            revenue = []

        a = range(len(Oth))
        for i in range(len(year)):
            try:
                data = {'Ticker':(ticker),'Total revenue':Oth[0][i],'YoY growth Total revenue':YoY[0][i],
                    'Cost of goods sold':Oth[1][i],
                    'Gross profit':Oth[2][i],'YoY growth Gross profit':YoY[2][i],
                    'Operating expenses (excl. COGS)':Oth[3][i],
                    'Operating income':Oth[4][i],'YoY growth Operating income' : YoY[4][i],
                    'Non-operating income, total':Oth[5][i],
                    'Pretax income':Oth[6][i],'YoY growth Pretax income':YoY[6][i],
                    'Equity in earnings':Oth[7][i],'Taxes':Oth[8][i],
                    'Non-controlling/minority interest':Oth[9][i],'After tax other income/expense':Oth[10][i],
                    'Net income before discontinued operations':Oth[11][i],'Discontinued operations':Oth[12][i],
                    'Net income':Oth[13][i],'YoY growth Net income':YoY[13][i],
                    'Dilution adjustment':Oth[14][i],'Preferred dividends':Oth[15][i],'Diluted net income available to common stockholders':Oth[16][i],
                    'Basic EPS':Oth[17][i],'YoY growth Basic EPS':YoY[17][i],'Diluted EPS':Oth[18][i],'Diluted EPS YoY growth':YoY[18][i],
                    'Average basic shares outstanding':Oth[19][i],'Diluted shares outstanding':Oth[20][i],
                    'EBITDA':Oth[21][i],'YoY growth EBITDA':YoY[21][i],'EBIT':Oth[22][i],'YoY growth EBIT': YoY[22][i],
                    'Total operating expenses':Oth[23][i],'Quarterly':year[i]}
                thf = pd.DataFrame(data,index=[i])
                thf2 = pd.concat([thf2,thf],ignore_index=True)
            except:
                print(i)
                print('error here')
        count = 0
        year = []
        if save == True:
            thf2.to_sql('stock_quarter',con=conn,if_exists='append',index=False)
        return thf2
    
    def update_quarter(self,ticker):
        thf2 = self.download_quarter(ticker,False)
        a = len(thf2)
        conn = sqlite3.connect("stock.sqlite")
        count = 1
        query = "SELECT Quarterly FROM stock_quarter WHERE `Ticker` == '%s'" % ticker
        test = pd.read_sql(query, conn).values.tolist()[-1]
        q = thf2['Quarterly']
        for i in range(a):
            if [list(thf2['Quarterly'].values)[i]] == test :
                break
            count += 1
        data = thf2.iloc[count:,:]
        data.to_sql('stock_quarter',con=conn,if_exists='append',index=False)
        return data
    
    def update_year(self,ticker):
        thf2 = self.download_year(ticker,False)
        a = len(thf2)
        conn = sqlite3.connect("stock.sqlite")
        count = 1
        query = "SELECT Year FROM stock_financial WHERE `Ticker` == '%s'" % ticker
        test = pd.read_sql(query, conn).values.tolist()[-1]
        q = thf2['Year']
        for i in range(a):
            if [list(thf2['Year'].values)[i]] == test :
                break
            count += 1
        data = thf2.iloc[count:,:]
        data.to_sql('stock_financial',con=conn,if_exists='append',index=False)
        return data

    def download_new_stock(self,Ticker):
        a = self.download_info(Ticker)
        b = self.download_stock(Ticker)
        c = self.download_year(Ticker,True)
        d = self.download_quarter(Ticker,True)
        # e = news_one_Nasdaq(Ticker) # <---- ยังไม่ได้ลอง
        # g = download_place(Ticker) # <---- ยังไม่ได้ลอง
    
    def growth_rate(self,Ticker,period):
        conn = sqlite3.connect("stock.sqlite")
        if period == 'Hour':
            query = "SELECT Datetime,Open,Close FROM stock_table_hr WHERE [Ticker] = '%s'" % Ticker
        elif period == 'Day':
            query = "SELECT Datetime,Open,Close FROM stock_table_d WHERE [Ticker] = '%s'" % Ticker
        elif period == 'Month':
            query = "SELECT Datetime,Open,Close FROM stock_table_mo WHERE [Ticker] = '%s'" % Ticker
        else:
            return False
        stock = pd.read_sql(query,conn)
        try:
            Open = stock.tail(1)['Open'].values.tolist()[0]
            Close = stock.tail(1)['Close'].values.tolist()[0]
        except:
            return False
        Diff = pd.DataFrame({'Ticker': [Ticker],'Diff':[int((Close-Open)*100)/100], 'Ratio': [str(int(((Close-Open)/Close)*10000)/100) + '%']})
        return Diff

    def All_growth_rate(self,period):
        Ticker = self.getAllticker()
        df2 = pd.DataFrame()
        for i in Ticker:
            df = self.growth_rate(i,period)
            if (df.bool()):
                return False
            else:
                df2 = pd.concat([df2,df],ignore_index=True)
        return df2