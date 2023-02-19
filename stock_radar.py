import unittest
from unittest.mock import patch,MagicMock , Mock
import sqlite3
import pandas as pd
import datetime
import yfinance as yf
from pandas.testing import assert_frame_equal
# from jupyter_dash import JupyterDash
from dash import Dash, html, dcc, Input, Output, callback , State, ctx, dash_table
import dateutil.relativedelta
from datetime import date
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
from bs4 import BeautifulSoup


class TestMLStock(unittest.TestCase):
    def setUp(self):
        self.stock = ML_stock('ABC')

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_getLastDate(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC'], 'Datetime': ['2022-01-01 10:00:00'], 'industryGroup': ['industry'], 'sector': ['sector']})
        mock_read_sql.return_value = df

        # Call the method being tested
        result = self.stock.getLastDate('Hour')

        # Make assertions about the result
        self.assertEqual(result, ['2022', '01', '01'])
    
    @patch('datetime.datetime')
    def test_getDiffDay_sameDay(self, mock_datetime):
        #Set last date
        self.stock.LastDate = ['2022', '01', '01']  # Set the LastDate attribute to a known value
        # Set date time
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2022
        mock_now.month = 1
        mock_now.day = 1

        # Call the method being tested
        result = self.stock.getDiffDay()

        # Make assertions about the result
        self.assertEqual(result, '0d')

    @patch('datetime.datetime')
    def test_getDiffDay_OneYear(self, mock_datetime):
        self.stock.LastDate = ['2022', '1', '1']  # Set the LastDate attribute to a known value
        # Set date time
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2023
        mock_now.month = 1
        mock_now.day = 1

        # Call the method to tested
        result = self.stock.getDiffDay()

        # assertions about the result
        self.assertEqual(result, '365d')

    @patch('yfinance.download')
    @patch('sqlite3.connect')
    def test_update(self, mock_connect, mock_download):
        # Set lastdate ind sec
        self.stock.LastDate = ['2022', '01', '01']  # Set the LastDate attribute to a known value
        self.stock.r_df = pd.DataFrame({'ticker': ['ABC'], 'Datetime': ['2022-01-01 10:00:00']})
        # Set up the mock cursor
        mock_conn = MagicMock()
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01 10:00:00')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC']}, index=[datetime.datetime(2022, 1, 1)])
        mock_download.return_value = df
        # Set up the mock DataFrame returned by the update method
        mock_data = df
        # Set up the mock to_sql method of mock_data
        mock_data.to_sql = MagicMock()

        # Call the method being tested
        result = self.stock.update('ABC', 'Hour')
        mock_data.to_sql('stock_table', con=mock_conn, if_exists='append', index=True)
        # Make assertions about the result
        assert_frame_equal(result, mock_data)
        # self.assertTrue(result.equals(df))
        mock_download.assert_called_once_with(tickers='ABC', period=self.stock.DiffDay, interval='1h')
        mock_data.to_sql.assert_called_once_with('stock_table', con=mock_conn, if_exists='append', index=True)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_getAllticker(self,mock_read_sql,mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'Ticker': ['ABC','KKK'], 'Datetime': ['2022-01-01 10:00:00','2022-01-01 10:00:00'], 'industryGroup': ['industry','industry'], 'sector': ['sector','sector']},)
        mock_read_sql.return_value = df
        
        # Call the method being tested
        result = self.stock.getAllticker('Test')

        # Make assertions about the result
        self.assertEqual(result,['ABC','KKK'])

    @patch('yfinance.download')
    @patch('sqlite3.connect')
    def test_download(self,mock_connect,mock_download):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC']}, index=[datetime.datetime(2022, 1, 1)])
        mock_download.return_value = df
        # Set up the mock DataFrame returned by the download method
        mock_data = df
        # Call the method being tested
        result = self.stock.download_ticker('Hour','DELTA.BK')

        # Make assertions about the result
        assert_frame_equal(result,mock_data)


    @patch('pandas.read_sql')
    def test_list_set(self, mock_read_sql):
        # Set up the mock cursor
        # Set up the mock DataFrame
        df = pd.DataFrame({'Ticker': ['AAV', 'ACE', 'ADVANC', 'AMATA', 'AOT', 'AP', 'AWC', 'BAM', 'BANPU', 'BBL', 'BCH', 'BCP', 'BCPG', 
                                        'BDMS', 'BEC', 'BEM', 'BGRIM', 'BH', 'BLA', 'BTS', 'BYD', 'CBG', 'CENTEL', 'CHG', 'CK', 'CKP', 'COM7', 
                                        'CPALL', 'CPF', 'CPN', 'CRC', 'DELTA', 'DOHOME', 'DTAC', 'EA', 'EGCO', 'EPG', 'ESSO', 'FORTH', 'GLOBAL', 
                                        'GPSC', 'GULF', 'GUNKUL', 'HANA', 'HMPRO', 'INTUCH', 'IRPC', 'IVL', 'JAS', 'JMART', 'JMT', 'KBANK', 'KCE', 
                                        'KEX', 'KKP', 'KTB', 'KTC', 'LH', 'MEGA', 'MINT', 'MTC', 'NEX', 'ONEE', 'OR', 'ORI', 'OSP', 'PLANB', 'PSL', 
                                        'PTG', 'PTT', 'PTTEP', 'PTTGC', 'QH', 'RATCH', 'RBF', 'RCL', 'SABUY', 'SAWAD', 'SCB', 'SCC', 'SCGP', 'SINGER', 
                                        'SPALI', 'SPRC', 'STA', 'STARK', 'STGT', 'TCAP', 'THANI', 'THG', 'TIDLOR', 'TIPH', 'TISCO', 'TOP', 'TQM', 'TRUE', 
                                        'TTB', 'TU', 'VGI', 'WHA']})
        mock_read_sql.return_value = df

        
        # Call the method being tested
        result = self.stock.list_set()
        
        # Make assertions about the result
        self.assertEqual(result,['AAV', 'ACE', 'ADVANC', 'AMATA', 'AOT', 'AP', 'AWC', 'BAM', 'BANPU', 'BBL', 'BCH', 'BCP', 'BCPG', 
                                             'BDMS', 'BEC', 'BEM', 'BGRIM', 'BH', 'BLA', 'BTS', 'BYD', 'CBG', 'CENTEL', 'CHG', 'CK', 'CKP', 'COM7', 
                                             'CPALL', 'CPF', 'CPN', 'CRC', 'DELTA', 'DOHOME', 'DTAC', 'EA', 'EGCO', 'EPG', 'ESSO', 'FORTH', 'GLOBAL', 
                                             'GPSC', 'GULF', 'GUNKUL', 'HANA', 'HMPRO', 'INTUCH', 'IRPC', 'IVL', 'JAS', 'JMART', 'JMT', 'KBANK', 'KCE', 
                                             'KEX', 'KKP', 'KTB', 'KTC', 'LH', 'MEGA', 'MINT', 'MTC', 'NEX', 'ONEE', 'OR', 'ORI', 'OSP', 'PLANB', 'PSL', 
                                             'PTG', 'PTT', 'PTTEP', 'PTTGC', 'QH', 'RATCH', 'RBF', 'RCL', 'SABUY', 'SAWAD', 'SCB', 'SCC', 'SCGP', 'SINGER', 
                                             'SPALI', 'SPRC', 'STA', 'STARK', 'STGT', 'TCAP', 'THANI', 'THG', 'TIDLOR', 'TIPH', 'TISCO', 'TOP', 'TQM', 'TRUE', 
                                             'TTB', 'TU', 'VGI', 'WHA'])


    @patch('sqlite3.connect')
    @patch('pandas.DataFrame.to_sql')   
    def test_save_data_news(self, mock_to_sql, mock_connect):
        # Create a sample DataFrame with some test data
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

        # Replace the real to_sql() method with the mock object
        mock_to_sql.return_value = None

        # Replace the real sqlite3.connect() method with the mock object
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # call the save_data_to_database function with some data
        self.stock.save_data_news(df)

        # Ensure that the connect() method was called with the correct database name
        mock_connect.assert_called_once_with('stock.sqlite')

        # Ensure that the to_sql() method was called with the correct table name and data
        expected_table = 'stock_news'
        expected_if_exists = 'append'
        expected_index = False
        mock_to_sql.assert_called_once_with(expected_table, con=mock_conn, if_exists=expected_if_exists, index=expected_index)

    @patch('sqlite3.connect')
    def test_load_data_news(self, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchall.return_value = ['2022-01-01', 'ABC', 'URL', 'Ticker']

        # Call the method being tested
        result = self.stock.load_data_news('2022-01-01', 'ABC', 'URL', 'Ticker')

        self.assertEqual(result, mock_cursor.fetchall.return_value)

    @patch('requests.get')
    def test_find_link(self, mock_get):
        # Define mock response object
        mock_response = Mock()
        mock_response.content = """
            <html>
            <body>
            <div class="tie-col-md-11 tie-col-sm-10 tie-col-xs-10">
            <a href="https://www.example.com/page1">Link 1</a>
            </div>
            <div class="tie-col-md-11 tie-col-sm-10 tie-col-xs-10">
            <a href="https://www.example.com/page2">Link 2</a>
            </div>
            </body>
            </html>
        """

        # Set up mock response from requests.get
        mock_get.return_value = mock_response

        # Call find_link function with mocked response
        result = self.stock.find_link("https://www.example.com")

        self.assertEqual(result, ["https://www.example.com/page1", "https://www.example.com/page2"])

    @patch('requests.get')
    def test_not_find_link(self, mock_get):
        # Define mock response object
        mock_response = Mock()
        mock_response.content = """
            <html>
            <body>
            <div class="tie-col-md-11 tie-col-sm-10">
            </div>
            <div class="tie-col-md-11 tie-col-sm-10">
            </div>
            </body>
            </html>
        """

        # Set up mock response from requests.get
        mock_get.return_value = mock_response

        # Call find_link function with mocked response
        result = self.stock.find_link("https://www.example.com")

        self.assertEqual(result, False)

    @patch('stock_radar.find_link')
    def test_scrap_news_SET(self, mock_find_link):
        mock_find_link.return_value = ['https://example.com']
        
        stock = ['PTT', 'ACE']
        
        title = 'Example News Title'
        date = '2022/02/20'
        body = 'Example news body'
        ticker = 'PTT'
        
        expected_df = pd.DataFrame({'Datetime': [datetime(2022, 2, 20)], 'Title':[title], 'Link':['https://example.com'], 'Body':[body], 'Ticker':[ticker+'.BK']})
        
        with patch('requests.get') as mock_requests:
            with patch('load_data_news') as mock_load_data_news:
                with patch('save_data_news') as mock_save_data_news:
                    mock_requests.return_value.content = f'<div class="post-title entry-title">{title}</div> <div class="date meta-item tie-icon">{date}</div> <div class="entry-content entry clearfix">{body}</div>'
                    mock_load_data_news.return_value = []
                    
                    self.stock.scrap_news_SET('https://example.com', stock)
                    
                    mock_load_data_news.assert_called_once_with(datetime(2022, 2, 20), title, 'https://example.com', ticker)
                    mock_save_data_news.assert_called_once_with(expected_df)

class ML_stock:
    def __init__(self,Company):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.Company = Company
        self.stock = []

    def getLastDate(self,period):
        conn = sqlite3.connect("stock.sqlite")
        # Query last element of stock in database
        if period == 'Hour':query = "SELECT * FROM stock_table_hr WHERE `ticker` = '%s'" % self.Company
        elif period == 'Day':query = "SELECT * FROM stock_table_d WHERE `ticker` = '%s'" % self.Company
        elif period == 'Mount':query = "SELECT * FROM stock_table_mo WHERE `ticker` = '%s'" % self.Company
        self.r_df = pd.read_sql(query, conn)
        # Cut data to get only datatime
        last = self.r_df.tail(1).Datetime.to_string().split()
        self.LastDate = last[1].split()[0].split('-')
        return self.LastDate

    def getDiffDay(self):
        # Get datetime for now
        x = datetime.datetime.now()
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
        self.DiffDay = str(DiffDay) + 'd'
        return self.DiffDay
        
        
    def update(self,ticker,period):
        down = 0
        count = 0
        conn = sqlite3.connect("stock.sqlite")
        # Select period to download
        if period == 'Hour':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1h')
        elif period == 'Day':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1d')
        elif period == 'Mount':data = yf.download(tickers=ticker, period=self.DiffDay, interval='1mo')
        # Get number of extra stock
        for i in data.index.day:
            if data.index.year[count] == int(self.LastDate[0]):
                if data.index.month[count] == int(self.LastDate[1]):
                    if i == int(self.LastDate[2])+1 or i == int(self.LastDate[2])+2 or i == int(self.LastDate[2])+3:
                        break
            count += 1
        #for get extra time in database
        ok = self.r_df.tail(1).Datetime.to_string().split()[2]
        if ok == '10:00:00':down = 5
        elif ok == '11:00:00':down = 4
        elif ok == '12:00:00':down = 3
        elif ok == '14:00:00':down = 2
        elif ok == '15:00:00':down = 1
        elif ok == '16:00:00':down = 0
        # Cut extra stock off
        count = count - down
        data['ticker'] = ticker
        data = data.iloc[count:,:]
        # Select period to download and Save to sqlite
        if period == 'Hour':data.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        elif period == 'Day':data.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        elif period == 'Mount':data.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)
        return data

    def savetoDB(self,period,data):
        conn = sqlite3.connect("stock.sqlite")
        if period == 'Hour':data.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        elif period == 'Day':data.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        elif period == 'Mount':data.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)
    def getAllticker(self,period):
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        if period == 'Hour':
            query = "select distinct Ticker from stock_table_hr"
        elif period == 'Day':
            query = "select distinct Ticker from stock_table_d"
        elif period == 'Mount':
            query = "select distinct Ticker from stock_table_mo"
        else:
            query = ""
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
            elif period == 'Mount':
                data = yf.download(tickers=ticker, period='max', interval='1mo')
            else:
                data = None
            # Save to sqlite3
            data.to_sql('stock_table',con=conn,if_exists='append',index=True)
            # return data to ploting graph
            return data
        except:
            return False
        
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
            query = "SELECT * FROM stock_news WHERE DATETIME = '%s' AND Title = '%s' AND Link = '%s' AND Ticker = '%s'" %(date, title, url, ticker)
            cur.execute(query)
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

    
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
