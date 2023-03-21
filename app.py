from flask import Flask
import threading

from dash import Dash, html, dcc, Input, Output, callback , State, ctx, dash_table
import dash_bootstrap_components as dbc
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
import locationtagger
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

import time

from selenium import webdriver
from selenium.webdriver.common.by import By 
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtCore import QUrl, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog

import pandas_datareader as pdr
import ccxt

server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.SLATE])
index = ''

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
            self.LastDate = False
        return self.LastDate

    def getDiffDay(self):
        # Get datetime for now
        x = dt.datetime.now()
        if self.LastDate == False:
            self.DiffDay = False
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
        if self.DiffDay == False:
            return False
        query = "SELECT `Index` FROM stock_info WHERE `ticker` = '%s'" % ticker
        for_ind = pd.read_sql(query, conn)
        ok = self.r_df.tail(1).Datetime.to_string().split()[2]
        #for get extra time in database
        if for_ind['Index'].values == 'NASDAQ':
            self.DiffDay = str(self.DiffDay+1)+'d'
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
        if self.DiffDay == False:
            return False
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

    ##No test
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
        try:
            conn = sqlite3.connect("stock.sqlite")
            cur = conn.cursor()
            query = "select Ticker from stock_info where `Index` == 'SET100'"
            stock = pd.read_sql(query,conn)
            stock = list(stock['Ticker'])
            for i in stock:
                temp = i.split('.')
                self.stock.append(temp[0])
            return self.stock
        except:
            return False
    
    #return all stock in NASDAQ
    def list_nasdaq(self):
        self.stock = []
        try:
            conn = sqlite3.connect("stock.sqlite")
            cur = conn.cursor()
            query = "select Ticker from stock_info where `Index` == 'NASDAQ'"
            stock = pd.read_sql(query,conn)
            self.stock = list(stock['Ticker'])
            return self.stock
        except:
            return False
    
    #return all Crypto100 
    def list_crypto(self):
        self.stock = []
        try:
            conn = sqlite3.connect("stock.sqlite")
            cur = conn.cursor()
            query = "select Ticker from stock_info where `Index` == 'CRYPTO100'"
            stock = pd.read_sql(query,conn)
            stock = list(stock['Ticker'])
            for i in stock:
                temp = i.split('-')
                self.stock.append(temp[0])
            return self.stock
        except:
            return False

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
    
    ##No test
    #scrap news from API
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
        
    ##No test
    def D_news_one_Nasdaq(self,ticker):
        try:
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
                df = pd.DataFrame({'Datetime': [date_obj], 'Title':[title], 'Link':[get_url], 'Body':[body], 'Ticker':[ticker]})
                print(df)
                self.save_data_news(df)
            return True
        except:
            return False
        
    #scrap news from API
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
                        self.save_data_news(df)
            return True
        except: 
            self.news_Nasdaq(ind)

    ##No test
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
    def news_Crypto(self, interger):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        try:
            for i in self.stock[interger:]:
                ind = self.stock.index(i)
                cryp = i.split('-')
                cryp = cryp[0]
                # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
                url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&blockchain='+ cryp +'&limit=200&apikey=8X8QE27D001F3TV'
                r = requests.get(url)
                data = r.json()
                round = int(data['items'])
                for j in range(round):
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

    ##No test
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
    
    def get_latlong_for_all_content(self,df):
        self.place = pd.DataFrame()
        a = len(df)
        for i in range(a):
            data = self.getcity_and_latlong(df.iloc[i]['Body'])
            data['Datetime'] = df.iloc[i]['Datetime']
            data['Ticker'] = df.iloc[i]['Ticker']
            self.place = pd.concat([self.place,data],ignore_index=True)
        return self.place
    
    def get_poppulate_for_city(self):
        self.add = self.place.groupby(self.place.columns.tolist(),as_index=False).size()
        self.add.rename(columns={'size': 'population'}, inplace=True)
        return self.add

    #No test
    #Not finish
    def updateAll(self):
        period = ['Hour','Day','Month']
        Ticker = self.getAllticker()
        # self.News_SET100()
        # self.news_Nasdaq(0)
        # self.news_Crypto(0)
        for  i in Ticker:
            # self.update_place(i)
            try:
                for j in period:
                    self.getLastDate(j,i)
                    self.getDiffDay()
                    self.check_stock(i)
                    self.update(j,i)
            except:
                pass
        
    #Function for GUI       
    def stock_info(self,ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_info where Ticker = '"+ticker+"';",con)
        data = data.drop(columns=['Ticker'])
        return data

    #Function for GUI 
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

    #Function for GUI 
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

    #Function for GUI 
    def table_news(self, ticker):
        con = sqlite3.connect("stock.sqlite")
        cur = con.cursor()
        data = pd.read_sql("SELECT * FROM stock_news where Ticker = '"+ticker+"' order by Datetime desc;",con)
        data = data.drop(columns=['Ticker'])
        return data

    #Function for GUI 
    def plot(self, ticker, interval):
        now = dt.datetime.now()
        last_month = now + dateutil.relativedelta.relativedelta(months=-3)
        seven_month = now + dateutil.relativedelta.relativedelta(years=-3)
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
            
            if ticker in self.list_nasdaq():
                df_resample_hr = Hr.resample('30T').max()
                merged_index_hr  = Hr.index.append(df_resample_hr.index)
                timegap_hr = merged_index_hr[~merged_index_hr.duplicated(keep = False)]
                fig.update_xaxes( rangebreaks=[ dict(values = timegap_hr, dvalue = 30*60*1000 ,pattern='hour') ])

            else:
                df_resample_hr = Hr.resample('H').max()
                merged_index_hr  = Hr.index.append(df_resample_hr.index)
                timegap_hr = merged_index_hr[~merged_index_hr.duplicated(keep = False)]
                fig.update_xaxes(rangebreaks=[dict(values=timegap_hr, dvalue=3600000)])
            fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
            fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=5, label="5d", step="day", stepmode="backward"),
                        dict(count=10, label="10d", step="day", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                row=3,
                col=1
            )         
              
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
            fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
            fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                row=3,
                col=1
            )

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
            fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
            fig.update_xaxes(rangeslider_visible=False, row=2, col=1)
            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=3, label="3y", step="year", stepmode="backward"),
                        dict(count=6, label="6y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                row=3,
                col=1
            )

        fig.update_xaxes(rangemode="nonnegative")
        fig.update_yaxes(fixedrange=False)
        
        fig.update_layout(hovermode = "x", plot_bgcolor='#26262e', paper_bgcolor='#272B30',font_color='white')
        fig.update(layout_xaxis_rangeslider_visible=False)
        return fig
    
    #Function for GUI 
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
        try:
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
        except:
            return False
        return place
    
    def update_place(self,ticker):
        try:
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
        except:
            return False

    def download_info(self,Ticker):
        conn = sqlite3.connect("stock.sqlite")
        op = webdriver.ChromeOptions()
        op.add_argument('headless') 
        driver = webdriver.Chrome(options=op)
        df2 = pd.DataFrame()
        InsSec = []
        index = []
        try:
            driver.get("https://finance.yahoo.com/quote/%s/profile?p=%s"% (Ticker,Ticker))
            numlink = driver.find_elements(By.XPATH, '//span[@class="Fw(600)"]')
            for i in numlink[:2]:
                InsSec.append(i.text)
            driver.get("https://www.tradingview.com/symbols/%s/financials-income-statement/"% Ticker)
            Ilink = driver.find_elements(By.XPATH, '//*[@id="js-category-content"]/div[1]/div[1]/div/div/div/div[2]/button[2]/span[1]/span/span/div/span[1]')
            for i in Ilink:
                index.append(i.text)
            df1 = pd.DataFrame({'Ticker': [Ticker], 'Industry Group': [InsSec[0]], 'Sector': [InsSec[1]], 'Index': index})
            df1.to_sql('stock_info',con=conn,if_exists='append',index=False)
            return df1
        except:
            return df2

    def download_stock(self,Ticker):
        conn = sqlite3.connect("stock.sqlite")
        df_h = yf.download(tickers=Ticker, period='2y', interval='1h')
        df_h['Ticker'] = Ticker
        df_d = yf.download(tickers=Ticker, period='10y', interval='1d')
        df_d['Ticker'] = Ticker
        df_d.index.names = ['Datetime']
        try:
            df_mo = yf.download(tickers=Ticker, period='max', interval='1mo')
            df_mo['Ticker'] = Ticker
            df_mo.index.names = ['Datetime']
        except:
            df_mo = yf.download(tickers=Ticker, period='15y', interval='1mo')
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
        tickerest = ticker.split('.')[0]
        driver.get('https://www.tradingview.com/symbols/%s/financials-income-statement/'% tickerest)
        time.sleep(2)
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
        try:
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
        except:
            return False
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
        tickerest = ticker.split('.')[0]
        driver.get('https://www.tradingview.com/symbols/%s/financials-income-statement/'% tickerest)
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
        try:
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
        except:
            return False
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
        try:
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
        except:
            return False
    
    def update_year(self,ticker):
        try:
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
        except:
            return False

    def download_new_stock(self,Ticker):
        a = self.download_info(Ticker)
        if a.empty:
            return False
        b = self.download_stock(Ticker)
        c = self.download_year(Ticker,True)
        d = self.download_quarter(Ticker,True)
        if Ticker in self.list_nasdaq():
            e = self.news_one_Nasdaq(Ticker)
        elif Ticker in self.list_crypto():
            g = self.news_one_Crypto(Ticker)
        h = self.download_place(Ticker)
    
    def change_stock(self,Ticker,period):
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

    def All_change_stock(self,period):
        Ticker = self.getAllticker()
        df2 = pd.DataFrame()
        for i in Ticker:
            df = self.change_stock(i,period)
            if (df.bool()):
                return False
            else:
                df2 = pd.concat([df2,df],ignore_index=True)
        return df2

stock = ML_stock()
######DASH######
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.ConfirmDialog(
        id='confirm-danger',
        message='Not found that tickers\nDo you want to download',
    ),
    dcc.ConfirmDialog(
        id='confirm-download',
        message='Finished',
    ),
    dcc.ConfirmDialog(
        id='failed-download',
        message='Failed to download',
    ),
    html.Div(id='page-content',),
    dcc.Store(id='memory')
])

# #loading screen
# @app.callback(
#     Output("loading-output", "children"),
#     [Input("submit-button", "n_clicks")]
# )
# def load_output(n_clicks):
#     if n_clicks:
#         time.sleep(2)
#         return 'Download finish'
#     return ''

#show dialog no ticker
@app.callback(Output('confirm-danger', 'displayed'),
              [Input('submit-button', 'n_clicks')],
              [State('ticker-input', 'value')],)
def display_confirm(n_clicks, value):
    tickers = stock.getAllticker()
    ticker = value.upper()
    print(ticker)
    if n_clicks != 0 and ticker not in tickers:
        return True
    return False

#show dialog download
@app.callback([Output('confirm-download', 'displayed'), 
               Output('memory', 'data')],
               [Input('confirm-danger', 'submit_n_clicks')],
               [State('ticker-input', 'value')])
def display_confirm(n_clicks, value):
    if n_clicks:
        result = stock.download_new_stock(value.upper())
        print(1)
        print(result)
        if result == False:
            return False, 'fail'
        return True, True
    return False, False

#failed to download
@app.callback(Output('failed-download', 'displayed'),
              [Input('memory', 'data')])
def display_confirm(data):
    print(data)
    print(2)
    if data == 'fail':
        return True
    return False

#return graph from ticker input
@app.callback(Output('graph','figure'),
              [Input('stock-dropdown', 'value'), 
              Input('submit-button', 'n_clicks'),
              Input('confirm-download', 'submit_n_clicks')],
              [State('ticker-input', 'value')])
def update_graph(stock_dropdown, submit_clicks, submit_n_clicks, ticker_input):
    global index
    global df 
    stock = ML_stock()
    df = stock.table_finance(ticker_input.upper())
    if "stock-dropdown" == ctx.triggered_id:
        print(ticker_input.upper())
        return dropdown_output(stock_dropdown, ticker_input.upper())
    elif "submit-button" == ctx.triggered_id:
        return update_output(ticker_input.upper())
    elif submit_n_clicks:
        return  dropdown_output('Hour', ticker_input.upper())

def update_output(ticker_input):
    stock = ML_stock()
    list_db = stock.stock_name()
    value = ticker_input.upper()
    if value.strip() == '' or (value.strip() not in list_db):
            fig = stock.plot('','Hour')
            return fig
    else:
        for i in ['Hour','Day','Month']:
            stock.getLastDate(i,value)
            stock.getDiffDay()
            print(stock.check_stock(value))
            print(stock.update(i,value))
        value = value.upper()
        fig = stock.plot(value,'')
        return fig

def dropdown_output(stock_dropdown ,ticker_input):
    global dropdown_value
    stock = ML_stock()
    dropdown_value = stock_dropdown
    value = str(ticker_input).upper()
    fig = stock.plot(value, stock_dropdown)
    return fig

# reset dropdown value
@app.callback(Output('stock-dropdown', 'value'),
              [Input('submit-button', 'n_clicks'),
               Input('confirm-download', 'submit_n_clicks')],
              [State('ticker-input', 'value')]
             )
def reset_dropdown(n_clicks, submit_n_clicks, value):
    if n_clicks:
        return None
    elif submit_n_clicks:
        return 'Hour'
    

# set display value
@app.callback(Output("disp-ticker", "children"),
              [Input('submit-button', 'n_clicks')],
              [State('ticker-input', 'value')]
             )
def reset_display(n_clicks, value):
    global index
    stock = ML_stock()
    tickers = stock.getAllticker()
    index = value
    if value.upper() not in tickers:
        return ''
    return value.upper()

#show diff and ratio
@app.callback(
    Output('growth-rate', 'children'),
    [Input('stock-dropdown', 'value'),
    Input('submit-button', 'n_clicks'),
    Input('confirm-download', 'submit_n_clicks')],
    [State('ticker-input', 'value')]
)
def show_table(stock_dropdown, submit_clicks, submit_n_clicks, ticker_input):
    stock = ML_stock()
    data = stock.change_stock(ticker_input.upper(), stock_dropdown)
    diff = data['Diff'][0]
    ratio = data['Ratio'][0]
    ratio = ratio.split('%')[0]
    ratio = float(ratio)
    if submit_clicks is not None:
        diff_color = 'green' if diff > 0 else 'red'
        ratio_color = 'green' if ratio > 0 else 'red'
        diff_output = html.Span('{:.2f}'.format(diff), style={'color': diff_color})
        ratio_output = html.Span('{:.2f}%'.format(ratio), style={'color': ratio_color})
        return html.Div([
            html.P('Difference: ', style={'display': 'inline-block', 'margin-right': '10px'}),
            diff_output,
            html.P('Ratio: ', style={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '10px'}),
            ratio_output
        ])
    elif submit_n_clicks:
        diff_color = 'green' if diff > 0 else 'red'
        ratio_color = 'green' if ratio > 0 else 'red'
        diff_output = html.Span('{:.2f}'.format(diff), style={'color': diff_color})
        ratio_output = html.Span('{:.2f}%'.format(ratio), style={'color': ratio_color})
        return html.Div([
            html.P('Difference: ', style={'display': 'inline-block', 'margin-right': '10px'}),
            diff_output,
            html.P('Ratio: ', style={'display': 'inline-block', 'margin-left': '20px', 'margin-right': '10px'}),
            ratio_output
        ])




#show table when press button
@app.callback(
    Output('disp-info', 'children'),
    [Input('submit-button', 'n_clicks'),
    Input('confirm-download', 'submit_n_clicks')],
    [State('ticker-input', 'value')]
)
def show_table(submit_clicks, submit_n_clicks, ticker_input):
    global index
    global df 
    stock = ML_stock()
    if submit_clicks is not None:
        df = stock.stock_info(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
            id='table-financial',
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            fill_width=False
        )
    elif submit_n_clicks:
        df = stock.stock_info(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
            id='table-financial',
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            fill_width=False
        )

#show table finance when press button
# @app.callback(
#     Output('table-container-home', 'children'),
#     [Input('submit-button', 'n_clicks')],
#     [State('ticker-input', 'value')]
# )
# def show_table(submit_clicks, ticker_input):
#     global index
#     global df 
#     stock = ML_stock()
#     if submit_clicks is not None:
#         df = stock.table_finance(ticker_input.upper())
#         return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
#             id='table-financial',
#             style_cell={
#                 'whiteSpace': 'normal',
#                 'height': 'auto'},
#             style_header={
#                 'backgroundColor': 'rgb(30, 30, 30)',
#                 'color': 'white'
#             },
#             style_data={
#                 'backgroundColor': 'rgb(50, 50, 50)',
#                 'color': 'white'
#             },
#             fill_width=False
#         )


#show table finance when press button
@app.callback(
    Output('table-container', 'children'),
    [Input('finance-dropdown', 'value'),
    Input('submit-button', 'n_clicks'),
    Input('confirm-download', 'submit_n_clicks')],
    [State('ticker-input', 'value')]
)
def show_table(stock_dropdown, submit_clicks, submit_n_clicks, ticker_input):
    global index
    global df 
    index = ticker_input.upper()
    stock = ML_stock()
    if stock_dropdown == 'Annual':
        stock.update_year(ticker_input.upper())
        df = stock.table_finance(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
            id='table-financial',
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            fill_width=False
        )
    elif stock_dropdown == 'Quarterly':
        stock.update_quarter(ticker_input.upper())
        df = stock.table_quarterly(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
            id='table-financial',
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            fill_width=False
        )
    
    if submit_n_clicks:
        stock.update_year(ticker_input.upper())
        df = stock.table_finance(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
            id='table-financial',
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            fill_width=False
        )

#show table news when press button
@app.callback(
    Output('news-container', 'children'),
    [Input('submit-button', 'n_clicks'),
     Input('confirm-download', 'submit_n_clicks')],
    [State('ticker-input', 'value')]
)
def show_table(submit_clicks, submit_n_clicks, ticker_input):
    global index
    global df 
    stock = ML_stock()
    if submit_clicks is not None:
        df = update_news(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"id": i, "name": i} for i in df.columns],
            id='news-financial',
            virtualization=True,
            fixed_rows={'header':True},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'minWidth':200,
                'width':200,
                'maxWidth':200,},
            #style_table={'height':500},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Link'},
                'width': '20%'},
                {'if': {'column_id': 'Title'},
                'width': '20%'},
                {'if': {'column_id': 'Datetime'},
                'width': '10%'},
            ],

        )
    elif submit_n_clicks:
        df = update_news(ticker_input.upper())
        return dash_table.DataTable(df.to_dict('records'), [{"id": i, "name": i} for i in df.columns],
            id='news-financial',
            virtualization=True,
            fixed_rows={'header':True},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'minWidth':200,
                'width':200,
                'maxWidth':200,},
            #style_table={'height':500},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Link'},
                'width': '20%'},
                {'if': {'column_id': 'Title'},
                'width': '20%'},
                {'if': {'column_id': 'Datetime'},
                'width': '10%'},
            ],

        )
    
def update_news(ticker_input):
    stock = ML_stock()
    set = stock.list_set()
    ticker = ticker_input
    nasdaq = stock.list_nasdaq()
    crypto = stock.list_crypto()
    ticker_input = ticker_input.split(".")
    ticker_input = ticker_input[0]
    print(ticker_input,set)
    print(ticker_input, nasdaq)
    print(crypto)
    if ticker_input in set:
        stock.News_SET100()
    elif ticker_input in nasdaq:
        stock.news_one_Nasdaq(ticker_input)
    elif ticker_input in crypto:
        stock.news_one_Crypto(ticker_input)
    return stock.table_news(ticker)

    
@app.callback(Output('graph-spartial','figure'),
              [Input('submit-button', 'n_clicks'),
               Input('confirm-download', 'submit_n_clicks')],
              [State('ticker-input', 'value')],)
def update_graph(submit_clicks, submit_n_clicks, ticker_input):
    global index
    global df 
    stock = ML_stock()
    df = stock.table_finance(ticker_input.upper())
    if submit_clicks is not None:
        return stock.plot_spatial(ticker_input.upper())
    if submit_n_clicks:
        return stock.plot_spatial(ticker_input.upper())
    

# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    stock = ML_stock()
    if pathname == '/graph':
        return html.Div(children=[
                    html.Div([
                        html.Div([
                            "Stock : ",
                            dcc.Input(id='ticker-input', value=index, type='text'),
                            html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        ],
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        dcc.Dropdown(['Hour', 'Day', 'Month'],
                            searchable=False,
                            id='stock-dropdown',
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        html.Div(id='output-div'),
                        html.Div(id="disp-ticker"),
                        ],
                        style={
                            'margin-top' : 50,
                            'margin-right': 100,
                            'margin-left': 100
                        }
                    ),
                    html.Div([
                        dcc.Graph(
                            id='graph',
                            figure=stock.plot('','Hour')
                        )],
                        style={
                                'margin-top' : 50,
                                'margin-right': 20,
                                'margin-left': 20,
                                'margin-bottom' : 50,
                        }
                    ),
                ])
    elif pathname == '/finance':
        return html.Div(children=[
                    html.Div([
                        html.Div([
                            "Stock : ",
                            dcc.Input(id='ticker-input', value=index, type='text'),
                            html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        ],
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        dcc.Dropdown(options=[{'label': 'Annual', 'value': 'Annual'}, {'label': 'Quarterly', 'value': 'Quarterly'}],
    value='Annual',
    searchable=False,
                            id='finance-dropdown',
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        html.Div(id='output-div'),
                        html.Div(id="disp-ticker"),
                        ],
                        style={
                            'margin-top' : 50,
                            'margin-right': 100,
                            'margin-left': 100
                        }
                    ),
                    html.Div(id='table-container'),
                ])
    elif pathname == '/news':
        return html.Div(children=[
                    html.Div([
                        
                        html.Div([
                            "Stock : ",
                            dcc.Input(id='ticker-input', value=index, type='text'),
                            html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        ],
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        
                        html.Div(id='output-div'),
                        html.Div(id="disp-ticker"),
                        ],
                        style={
                            'margin-top' : 50,
                            'margin-right': 100,
                            'margin-left': 100
                        }
                    ),
                    html.Div(id='news-container'),
                ])
    elif pathname == '/spartial':
        stock = ML_stock()
        return html.Div(children=[
                    html.Div([
                        html.Div([
                            "Stock : ",
                            dcc.Input(id='ticker-input', value=index, type='text'),
                            html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        ],
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        html.Div(id='output-div'),
                        html.Div(id="disp-ticker")
                        ],
                        style={
                            'margin-top' : 50,
                            'margin-right': 100,
                            'margin-left': 100
                        }
                    ),
                    html.Div([
                        dcc.Graph(
                            id='graph-spartial',
                            figure=stock.plot_spatial(''),
                        )],
                        style={
                                'margin-right': 20,
                                'margin-left': 20,
                                'width': '100vh', 
                                'height': '100vw'
                        }
                    ),
                ])
    else:
        stock = ML_stock()
        return html.Div(children=[
                    html.Div([
                        html.Div([
                            "Stock : ",
                            dcc.Input(id='ticker-input', value=index, type='text'),
                            html.Button(id='submit-button', n_clicks=0, children='Submit'),
                        ],
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        dcc.Dropdown(['Hour', 'Day', 'Month'],
                            searchable=False,
                            id='stock-dropdown',
                            style={
                                'margin-bottom': 20,
                            }
                        ),
                        html.Div(id='output-div'),
                        html.Div([  html.H2(index ,id="disp-ticker", style={'align-self': 'flex-start'}),
                                    html.Div(id="growth-rate", style={'align-self': 'flex-end'})
                                ], style={
                                    'display': 'flex',
                                    'flex-direction': 'row',
                                    'justify-content': 'space-between'
                                }),
                                html.Div(id="disp-info", style={'margin-top' : 20})
                        ],
                        style={
                            'margin-top' : 50,
                            'margin-right': 100,
                            'margin-left': 100
                        }
                    ),
                    # html.Div([
                    # dcc.DatePickerRange(
                    #     id='my-date-picker-range',
                    #     min_date_allowed=date(1995, 8, 5),
                    #     max_date_allowed=dt.datetime.now().date(),
                    #     initial_visible_month=dt.datetime.now().date(),
                    #     end_date=dt.datetime.now().date(),
                    #     style={
                    #         'margin-top' : 50,
                    #         'margin-right': 100,
                    #         'margin-left': 100,
                    #         'justify-content': 'center'
                    #     }
                    # )],
                    #     style={
                    #         'display': 'flex',
                    #         'flex-direction': 'column',
                    #         'align-items': 'flex-end',
                    #     }
                    # ),
                    html.Div([
                        dcc.Graph(
                            id='graph',
                            figure=stock.plot('','Hour')
                        )],
                        style={
                                'margin-top' : 20,
                                'margin-right': 20,
                                'margin-left': 20,
                                'margin-bottom' : 50,
                        }
                    ),
                ])
    # You could also return a 404 "URL not found" page here



class MyThread(QThread):
    finished = pyqtSignal()
    stock = ML_stock() 

    def __init__(self):
        super().__init__()

    def run(self):
        self.stock.updateAll()
        self.finished.emit()


class update_tickersThread(QThread):
    procress_updateticker = pyqtSignal(int)
    finished = pyqtSignal() 
    stock = ML_stock()

    def __init__(self):
        super().__init__()

    def run(self):
        period = ['Hour','Day','Month']
        tickers = self.stock.getAllticker()
        for  i in tickers:
            try:
                if tickers.index(i) == len(tickers)//4:
                    self.procress_updateticker.emit(25)
                elif tickers.index(i) == len(tickers)//2:
                    self.procress_updateticker.emit(50)
                elif tickers.index(i) == len(tickers)*3//4:
                    self.procress_updateticker.emit(75)
                for j in period:
                    self.stock.getLastDate(j,i)
                    self.stock.getDiffDay()
                    self.stock.check_stock(i)
                    self.stock.update(j,i)
            except:
                pass
        self.finished.emit()

class update_financialThread(QThread):
    procress_updatefinancial = pyqtSignal(int)
    finished = pyqtSignal() 
    stock = ML_stock()

    def __init__(self):
        super().__init__()

    def run(self):
        tickers = self.stock.getAllticker()
        for  i in tickers:
            try:
                self.stock.update_year(i)
                self.stock.update_quarter(i)
                if tickers.index(i) == len(tickers)//4:
                    self.procress_updatefinancial.emit(25)
                elif tickers.index(i) == len(tickers)//2:
                    self.procress_updatefinancial.emit(50)
                elif tickers.index(i) == len(tickers)*3//4:
                    self.procress_updatefinancial.emit(75)
            except:
                pass
        self.finished.emit()

class update_newsThread(QThread):
    procress_updatenews = pyqtSignal(int)
    finished = pyqtSignal() 
    stock = ML_stock()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.stock.News_SET100()
            self.procress_updatenews.emit(33)
            self.stock.list_nasdaq()
            self.stock.news_Nasdaq(0)
            self.procress_updatenews.emit(66)
            self.stock.list_crypto()
            self.stock.news_Crypto(0)
            self.procress_updatenews.emit(99)
        except:
            pass
        self.finished.emit()

class update_locationThread(QThread):
    procress_updatelocation = pyqtSignal(int)
    finished = pyqtSignal() 
    stock = ML_stock()

    def __init__(self):
        super().__init__()

    def run(self):
        tickers = self.stock.getAllticker()
        self.stock.News_SET100()
        self.procress_updatelocation.emit(20)
        self.stock.list_nasdaq()
        self.stock.news_Nasdaq(0)
        self.procress_updatelocation.emit(40)
        self.stock.list_crypto()
        self.stock.news_Crypto(0)
        self.procress_updatelocation.emit(60)
        for  i in tickers:
            try:
                if tickers.index(i) == len(tickers)//2:
                    self.procress_updatelocation.emit(80)
                self.stock.download_place(i)
            except:
                pass
        self.finished.emit()


url = 'http://127.0.0.1:5000'
class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1118, 779)
                MainWindow.setStyleSheet("background-color: rgb(10, 10, 28);\n"
                                         "color: rgb(255, 255, 255);\n"
                                          "border-radius: 10px;\n")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 781))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.verticalLayout.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
                self.label.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
        "color: rgb(255, 255, 255);")
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.verticalLayout.addWidget(self.label)
                self.pushButton_0 = QtWidgets.QPushButton(self.verticalLayoutWidget)
                self.pushButton_0.setEnabled(True)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pushButton_0.sizePolicy().hasHeightForWidth())
                self.pushButton_0.setSizePolicy(sizePolicy)
                self.pushButton_0.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "height: 50px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_0.setIconSize(QtCore.QSize(20, 20))
                self.pushButton_0.setObjectName("pushButton_0")
                self.verticalLayout.addWidget(self.pushButton_0)
                self.pushButton_1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
                self.pushButton_1.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "height: 50px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_1.setObjectName("pushButton_1")
                self.verticalLayout.addWidget(self.pushButton_1)
                self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
                self.pushButton_2.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "height: 50px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_2.setObjectName("pushButton_2")
                self.verticalLayout.addWidget(self.pushButton_2)
                self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
                self.pushButton_3.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "height: 50px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_3.setObjectName("pushButton_3")
                self.verticalLayout.addWidget(self.pushButton_3)
                self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
                self.pushButton_4.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "height: 50px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_4.setObjectName("pushButton_4")
                self.verticalLayout.addWidget(self.pushButton_4)
                self.frame_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.verticalLayout.addWidget(self.frame_2)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout.addItem(spacerItem)
                self.verticalLayout.setStretch(0, 2)
                self.verticalLayout.setStretch(1, 2)
                self.verticalLayout.setStretch(2, 2)
                self.verticalLayout.setStretch(3, 2)
                self.verticalLayout.setStretch(4, 2)
                self.verticalLayout.setStretch(7, 4)
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 0, 881, 781))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.frame = QtWidgets.QFrame(self.verticalLayoutWidget_2)
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame")
                self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
                self.stackedWidget.setGeometry(QtCore.QRect(20, 20, 841, 731))
                self.stackedWidget.setObjectName("stackedWidget")
                self.page = QtWidgets.QWidget()
                self.page.setObjectName("page")
                self.webView = QWebEngineView(self.page) 
                self.webView.setGeometry(QtCore.QRect(20, 20, 841, 731))
                self.webView.setObjectName("webView")
                self.webView.setUrl(QUrl(url+'//'))
                self.stackedWidget.addWidget(self.page)
                self.page_2 = QtWidgets.QWidget()
                self.page_2.setObjectName("page_2")
                self.frame_3 = QtWidgets.QFrame(self.page_2)
                self.frame_3.setGeometry(QtCore.QRect(-20, -20, 881, 771))
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.label_2 = QtWidgets.QLabel(self.frame_3)
                self.label_2.setGeometry(QtCore.QRect(380, 150, 141, 61))
                self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font: 12pt \"MS Shell Dlg 2\";")
                self.label_2.setObjectName("label_2")
                self.pushButton_6 = QtWidgets.QPushButton(self.frame_3)
                self.pushButton_6.setGeometry(QtCore.QRect(390, 420, 90, 50))
                self.pushButton_6.setStyleSheet("QPushButton {\n"
        "background-color: rgb(10, 10, 28);\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius: 10px;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "border: 1px solid white;\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(38, 38, 46);\n"
        "}")
                self.pushButton_6.setObjectName("pushButton_6")
                self.label_3 = QtWidgets.QLabel(self.frame_3)
                self.label_3.setGeometry(QtCore.QRect(350, 220, 170, 20))
                self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font: 10pt \"MS Shell Dlg 2\";")
                self.label_3.setText("")
                self.label_3.setObjectName("label_3")
                self.label_3.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar_1 = QtWidgets.QProgressBar(self.frame_3)
                self.progressBar_1.setGeometry(QtCore.QRect(310, 520, 261, 23))
                self.progressBar_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
                self.progressBar_1.setProperty("value", 0)
                self.progressBar_1.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar_1.setObjectName("progressBar")
                self.progressBar_2 = QtWidgets.QProgressBar(self.frame_3)
                self.progressBar_2.setGeometry(QtCore.QRect(310, 570, 261, 23))
                self.progressBar_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
                self.progressBar_2.setProperty("value", 0)
                self.progressBar_2.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar_2.setObjectName("progressBar_2")
                self.progressBar_3 = QtWidgets.QProgressBar(self.frame_3)
                self.progressBar_3.setGeometry(QtCore.QRect(310, 620, 261, 23))
                self.progressBar_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
                self.progressBar_3.setProperty("value", 0)
                self.progressBar_3.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar_3.setObjectName("progressBar_3")
                self.progressBar_4 = QtWidgets.QProgressBar(self.frame_3)
                self.progressBar_4.setGeometry(QtCore.QRect(310, 670, 261, 23))
                self.progressBar_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
                self.progressBar_4.setProperty("value", 0)
                self.progressBar_4.setAlignment(QtCore.Qt.AlignCenter)
                self.progressBar_4.setObjectName("progressBar_4")
                self.checkBox_1 = QtWidgets.QCheckBox(self.frame_3)
                self.checkBox_1.setGeometry(QtCore.QRect(400, 260, 70, 17))
                self.checkBox_1.setStyleSheet("color: rgb(255, 255, 255);")
                self.checkBox_1.setObjectName("checkBox_1")
                self.checkBox_2 = QtWidgets.QCheckBox(self.frame_3)
                self.checkBox_2.setGeometry(QtCore.QRect(400, 300, 70, 17))
                self.checkBox_2.setStyleSheet("color: rgb(255, 255, 255);")
                self.checkBox_2.setObjectName("checkBox_2")
                self.checkBox_3 = QtWidgets.QCheckBox(self.frame_3)
                self.checkBox_3.setGeometry(QtCore.QRect(400, 340, 70, 17))
                self.checkBox_3.setStyleSheet("color: rgb(255, 255, 255);")
                self.checkBox_3.setObjectName("checkBox_3")
                self.checkBox_4 = QtWidgets.QCheckBox(self.frame_3)
                self.checkBox_4.setGeometry(QtCore.QRect(400, 380, 70, 17))
                self.checkBox_4.setStyleSheet("color: rgb(255, 255, 255);")
                self.checkBox_4.setObjectName("checkBox_4")
                self.stackedWidget.addWidget(self.page_2)
                self.verticalLayout_2.addWidget(self.frame)
                MainWindow.setCentralWidget(self.centralwidget)

                myDialog = QDialog()
                myDialog.setObjectName("myDialog")


            
                myDialog.setStyleSheet("QDialog {\n"
            "background-color: rgb(165, 165, 168);\n"
            "color: rgb(255, 255, 255);\n"
            "border-radius: 10px;\n"
            "font: 10pt \"MS Shell Dlg 2\";\n"
            "border: 1px solid white;\n"
            "}\n")

                self.pushButton_0.clicked.connect(self.graph_page)
                self.pushButton_1.clicked.connect(self.financial_page)
                self.pushButton_2.clicked.connect(self.news_page)
                self.pushButton_3.clicked.connect(self.spartial_page)
                self.pushButton_4.clicked.connect(self.dashboard_page)
                self.pushButton_6.clicked.connect(self.startThread)

                self.retranslateUi(MainWindow)
                self.stackedWidget.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "ML Stock"))
                self.label.setText(_translate("MainWindow", "ML STOCK RADAR"))
                self.pushButton_0.setText(_translate("MainWindow", "Graph"))
                self.pushButton_1.setText(_translate("MainWindow", "Financial"))
                self.pushButton_2.setText(_translate("MainWindow", "News"))
                self.pushButton_3.setText(_translate("MainWindow", "Location"))
                self.pushButton_4.setText(_translate("MainWindow", "Update"))
                self.label_2.setText(_translate("MainWindow", "Update all data"))
                self.pushButton_6.setText(_translate("MainWindow", "Update"))
                self.checkBox_1.setText(_translate("MainWindow", "Ticker"))
                self.checkBox_2.setText(_translate("MainWindow", "Finacial"))
                self.checkBox_3.setText(_translate("MainWindow", "News"))
                self.checkBox_4.setText(_translate("MainWindow", "Location"))

                

        def startThread(self):
            self.threads = []
            self.texts = []
            self.progress = []
            if self.checkBox_1.isChecked():
                self.thread_1 = update_tickersThread()
                self.thread_1.finished.connect(self.threadFinished)
                self.thread_1.procress_updateticker.connect(self.thread_1Update)
                self.threads.append(self.thread_1)
                self.texts.append('Updating Ticker')
                self.progress.append(self.progressBar_1)
            if self.checkBox_2.isChecked():
                self.thread_2 = update_financialThread()
                self.thread_2.finished.connect(self.threadFinished)
                self.thread_2.procress_updatefinancial.connect(self.thread_2Update)
                self.threads.append(self.thread_2)
                self.texts.append('Updating Financial')
                self.progress.append(self.progressBar_2)
            if self.checkBox_3.isChecked():
                self.thread_3 = update_newsThread()
                self.thread_3.finished.connect(self.threadFinished)
                self.thread_3.procress_updatenews.connect(self.thread_3Update)
                self.threads.append(self.thread_3)
                self.texts.append('Updating News')
                self.progress.append(self.progressBar_3)
            if self.checkBox_4.isChecked():
                try:
                    index = self.threads.index(self.thread_3)
                    self.threads.pop(index)
                    self.texts.pop(index)
                    self.progress.pop(index)
                except:
                    pass
                self.thread_4 = update_locationThread()
                self.thread_4.finished.connect(self.threadFinished)
                self.thread_4.procress_updatelocation.connect(self.thread_4Update)
                self.threads.append(self.thread_4)
                self.texts.append('Updating Location')
                self.progress.append(self.progressBar_4)

            if len(self.threads) == 0:
                self.label_3.setText('Please select update')
            else:
                self.pushButton_6.setEnabled(False)
                self.checkBox_1.setEnabled(False)
                self.checkBox_2.setEnabled(False)
                self.checkBox_3.setEnabled(False)
                self.checkBox_4.setEnabled(False)
                self.pushButton_6.setStyleSheet("QPushButton {\n"
                    "background-color: rgb(165, 165, 168);\n"
                    "color: rgb(255, 255, 255);\n"
                    "border-radius: 10px;\n"
                    "font: 10pt \"MS Shell Dlg 2\";\n"
                    "border: 1px solid white;\n"
                    "}\n"
                )
                self.startNextThread()

        def startNextThread(self):
            if len(self.threads) > 0:
                thread = self.threads.pop(0)
                text = self.texts.pop(0)
                procress = self.progress[0]
                self.label_3.setText(text)
                procress.setProperty("value", 10)
                thread.start()
            else:
                self.label_3.setText('Finish')
                self.checkBox_1.setChecked(False)
                self.checkBox_2.setChecked(False)
                self.checkBox_3.setChecked(False)
                self.checkBox_4.setChecked(False)
                self.checkBox_1.setEnabled(True)
                self.checkBox_2.setEnabled(True)
                self.checkBox_3.setEnabled(True)
                self.checkBox_4.setEnabled(True)
                self.pushButton_6.setEnabled(True)
                self.pushButton_6.setStyleSheet("QPushButton {\n"
                    "background-color: rgb(10, 10, 28);\n"
                    "color: rgb(255, 255, 255);\n"
                    "border-radius: 10px;\n"
                    "font: 10pt \"MS Shell Dlg 2\";\n"
                    "border: 1px solid white;\n"
                    "}\n"
                )

        def threadFinished(self):
            procress = self.progress.pop(0)
            procress.setProperty("value", 100)
            self.startNextThread()

        def thread_1Update(self, value):
            procress = self.progress[0]
            procress.setProperty("value", value)

        def thread_2Update(self, value):
            procress = self.progress[0]
            procress.setProperty("value", value)

        def thread_3Update(self, value):
            procress = self.progress[0]
            procress.setProperty("value", value)

        def thread_4Update(self, value):
            procress = self.progress[0]
            procress.setProperty("value", value)

        


    
        def dashboard_page(self):
                self.stackedWidget.setCurrentIndex(1)

        def graph_page(self):
                self.stackedWidget.setCurrentIndex(0)
                self.webView.setUrl(QUrl(url+'//'))

        def financial_page(self):
                self.stackedWidget.setCurrentIndex(0)
                self.webView.setUrl(QUrl(url+'/finance'))

        def news_page(self):
                self.stackedWidget.setCurrentIndex(0)
                self.webView.setUrl(QUrl(url+'/news'))

        def spartial_page(self):
                self.stackedWidget.setCurrentIndex(0)
                self.webView.setUrl(QUrl(url+'/spartial'))

        def update_function(self):
            self.stock.updateAll()


if __name__ == "__main__":
    # Start Flask server with Dash in a separate thread
    flask_thread = threading.Thread(target=server.run, kwargs={"debug":False})
    flask_thread.start()

    pyapp = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(pyapp.exec_())


