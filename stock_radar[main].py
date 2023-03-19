import unittest
from unittest.mock import patch,MagicMock , Mock
from unittest import mock
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
import locationtagger
from geopy.geocoders import Nominatim
import translators as ts
import translators.server as tss
from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import pandas_datareader as pdr
import ccxt

class TestMLStock(unittest.TestCase):
    def setUp(self):
        self.stock = ML_stock()

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_getLastDate1(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC'], 'Datetime': ['2022-01-01 10:00:00'], 'industryGroup': ['industry'], 'sector': ['sector']})
        mock_read_sql.return_value = df

        # Call the method being tested
        result = self.stock.getLastDate('Hour','ABC')

        # Make assertions about the result
        self.assertEqual(result, ['2022', '01', '01'])
    
    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_getLastDate2(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC'], 'Datetime': [''], 'industryGroup': ['industry'], 'sector': ['sector']})
        mock_read_sql.return_value = df

        # Call the method being tested
        result = self.stock.getLastDate('Hour','ABC')

        # Make assertions about the result
        self.assertEqual(result, False)

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
        self.assertEqual(result, 0)

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
        self.assertEqual(result, 365)

    @patch('datetime.datetime')
    def test_getDiffDay_False(self, mock_datetime):
        self.stock.LastDate = False  # Set the LastDate attribute to a known value
        # Set date time
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2023
        mock_now.month = 1
        mock_now.day = 1

        # Call the method to tested
        result = self.stock.getDiffDay()

        # assertions about the result
        self.assertEqual(result, False)
    
    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_check_stock1(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'Index': ['NASDAQ']})
        mock_read_sql.return_value = df

        self.stock.r_df = pd.DataFrame({'Datetime': ['2023-02-13 11:30:00']})
        # Call the method being tested
        result = self.stock.check_stock('ABC')

        # Make assertions about the result
        self.assertEqual(result, 4)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_check_stock2(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value
        self.stock.DiffDay = 5
        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'Index': ['NASDAQ']})
        mock_read_sql.return_value = df

        self.stock.r_df = pd.DataFrame({'Datetime': ['2023-02-13 10:30:00']})
        # Call the method being tested
        result = self.stock.check_stock('ABC')

        # Make assertions about the result
        self.assertEqual(result, 5)
        self.assertEqual(self.stock.DiffDay, '5d')
    
    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_check_stock3(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value
        self.stock.DiffDay = 2
        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'Index': ['SET100']})
        mock_read_sql.return_value = df

        self.stock.r_df = pd.DataFrame({'Datetime': ['2023-02-13 10:00:00']})
        # Call the method being tested
        result = self.stock.check_stock('ABC')

        # Make assertions about the result
        self.assertEqual(result, 5)
        self.assertEqual(self.stock.DiffDay, '2d')

    @patch('sqlite3.connect')
    @patch('pandas.read_sql')
    def test_check_stock4(self, mock_read_sql, mock_connect):
        # Set up the mock cursor
        mock_cursor = mock_connect.return_value.cursor.return_value
        self.stock.DiffDay = 19
        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01', 'industry', 'sector')

        # Set up the mock DataFrame
        df = pd.DataFrame({'Index': ['CRYPTO100']})
        mock_read_sql.return_value = df

        self.stock.r_df = pd.DataFrame({'Datetime': ['2023-02-13 19:00:00']})
        # Call the method being tested
        result = self.stock.check_stock('ABC')

        # Make assertions about the result
        self.assertEqual(result, 4)
        self.assertEqual(self.stock.DiffDay, '20d')

    @patch('yfinance.download')
    @patch('sqlite3.connect')
    def test_update(self, mock_connect, mock_download):
        # Set lastdate ind sec
        self.stock.LastDate = ['2022', '01', '01']  # Set the LastDate attribute to a known value
        self.stock.r_df = pd.DataFrame({'ticker': ['ABC'], 'Datetime': ['2022-01-01 10:00:00']})
        self.stock.down = 0
        # Set up the mock cursor
        mock_conn = MagicMock()
        mock_cursor = mock_connect.return_value.cursor.return_value

        # Set the expected return value of the mock cursor
        mock_cursor.fetchone.return_value = ('ABC', '2022-01-01 10:00:00')

        # Set up the mock DataFrame
        df = pd.DataFrame({'ticker': ['ABC']}, index=[datetime.datetime(2022, 1, 2)])
        df.index.name = 'Datetime'
        mock_download.return_value = df
        # Set up the mock DataFrame returned by the update method
        mock_data = df
        # Set up the mock to_sql method of mock_data
        mock_data.to_sql = MagicMock()

        # Call the method being tested
        result = self.stock.update('Hour','ABC')
        mock_data.to_sql('stock_table', con=mock_conn, if_exists='append', index=True)
        # Make assertions about the result
        assert_frame_equal(result, mock_data)
        # self.assertTrue(result.equals(df))
        mock_download.assert_called_once_with(tickers='ABC', period=self.stock.DiffDay, interval='1h', progress=False)
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
        result = self.stock.getAllticker()

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
    def test_list_set_SET(self, mock_read_sql):
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
        
    @patch('pandas.read_sql')
    def test_list_set_NASDAQ(self, mock_read_sql):
        # Set up the mock cursor
        # Set up the mock DataFrame
        df = pd.DataFrame({'Ticker': ['ABNB', 'ADBE', 'ADI', 'ADSK', 'AEP', 'ALGN', 'AMAT', 'AMGN', 'ANSS', 'ATVI', 'AVGO', 'AZN', 'BIIB', 'BKNG', 'BKR', 
                                        'CEG', 'CHTR', 'COST', 'CPRT', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DLTR', 'DXCM', 'EA', 'EBAY', 'ENPH', 
                                        'EXC', 'FANG', 'FAST', 'FISV', 'FTNT', 'GOOG', 'GOOGL', 'HON', 'IDXX', 'ILMN', 'ISRG', 'JD', 'KHC', 'KLAC', 'LCID', 
                                        'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MSFT', 'MU', 'ODFL', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD', 
                                        'PEP', 'QCOM', 'REGN', 'RIVN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'TMUS', 'VRSK', 'VRTX', 'WDAY', 'XEL', 'ZM', 'ZS']})
        mock_read_sql.return_value = df

        
        # Call the method being tested
        result = self.stock.list_nasdaq()
        
        # Make assertions about the result
        self.assertEqual(result,['ABNB', 'ADBE', 'ADI', 'ADSK', 'AEP', 'ALGN', 'AMAT', 'AMGN', 'ANSS', 'ATVI', 'AVGO', 'AZN', 'BIIB', 'BKNG', 'BKR', 
                                'CEG', 'CHTR', 'COST', 'CPRT', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DLTR', 'DXCM', 'EA', 'EBAY', 'ENPH', 
                                'EXC', 'FANG', 'FAST', 'FISV', 'FTNT', 'GOOG', 'GOOGL', 'HON', 'IDXX', 'ILMN', 'ISRG', 'JD', 'KHC', 'KLAC', 'LCID', 
                                'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MSFT', 'MU', 'ODFL', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD', 
                                'PEP', 'QCOM', 'REGN', 'RIVN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'TMUS', 'VRSK', 'VRTX', 'WDAY', 'XEL', 'ZM', 'ZS'])

    @patch('pandas.read_sql')
    def test_list_set_CRYPTO(self, mock_read_sql):
        # Set up the mock cursor
        # Set up the mock DataFrame
        df = pd.DataFrame({'Ticker': ['BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'BUSD', 'ADA', 'DOGE', 'MATIC', 'HEX', 'SOL', 'DOT', 'SHIB', 'LTC', 'WTRX', 'TRX', 
                                      'AVAX', 'STETH', 'DAI', 'UNI7083', 'WBTC', 'ATOM', 'LINK', 'LEO', 'ETC', 'XMR', 'TON11419', 'OKB', 'BCH', 'APT21794', 'LDO', 
                                      'HBAR', 'XLM', 'FIL', 'NEAR', 'APE18876', 'CRO', 'ALGO', 'VET', 'QNT', 'ICP', 'GRT6719', 'FTM', 'MANA', 'TMG', 'BTCB', 'BIT11221', 
                                      'AAVE', 'EOS', 'WBNB', 'AXS', 'EGLD', 'FLOW', 'THETA', 'SAND', 'FRAX', 'LUNC', 'XTZ', 'TUSD', 'IMX10603', 'CHZ', 'MINA', 'HBTC', 
                                      'USDP', 'RPL', 'HT', 'KCS', 'CRV', 'BSV', 'FXS', 'DASH', 'ZEC', 'MKR', 'USDD', 'BTTOLD', 'BTT', 'CAKE', 'XEC', 'MIOTA', 'TNC5524', 
                                      'GMX11857', 'SNX', 'KLAY', 'BGB', 'NEO', 'TWT', 'GUSD', 'OP', 'RUNE', 'LRC', 'FTT', 'AGIX', 'PAXG', 'OSMO', 'XRD', 'BABYDOGE', 'GT', 'ZIL', 'CVX']})
        mock_read_sql.return_value = df

        
        # Call the method being tested
        result = self.stock.list_crypto()
        
        # Make assertions about the result
        self.assertEqual(result,['BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'BUSD', 'ADA', 'DOGE', 'MATIC', 'HEX', 'SOL', 'DOT', 'SHIB', 'LTC', 'WTRX', 'TRX', 
                                'AVAX', 'STETH', 'DAI', 'UNI7083', 'WBTC', 'ATOM', 'LINK', 'LEO', 'ETC', 'XMR', 'TON11419', 'OKB', 'BCH', 'APT21794', 'LDO', 
                                'HBAR', 'XLM', 'FIL', 'NEAR', 'APE18876', 'CRO', 'ALGO', 'VET', 'QNT', 'ICP', 'GRT6719', 'FTM', 'MANA', 'TMG', 'BTCB', 'BIT11221', 
                                'AAVE', 'EOS', 'WBNB', 'AXS', 'EGLD', 'FLOW', 'THETA', 'SAND', 'FRAX', 'LUNC', 'XTZ', 'TUSD', 'IMX10603', 'CHZ', 'MINA', 'HBTC', 
                                'USDP', 'RPL', 'HT', 'KCS', 'CRV', 'BSV', 'FXS', 'DASH', 'ZEC', 'MKR', 'USDD', 'BTTOLD', 'BTT', 'CAKE', 'XEC', 'MIOTA', 'TNC5524', 
                                'GMX11857', 'SNX', 'KLAY', 'BGB', 'NEO', 'TWT', 'GUSD', 'OP', 'RUNE', 'LRC', 'FTT', 'AGIX', 'PAXG', 'OSMO', 'XRD', 'BABYDOGE', 'GT', 'ZIL', 'CVX'])
    

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

    def test_scrap_news_SET_new_news(self):
        # Mock the return value of the find_link function
        mock_find_link = MagicMock(return_value=["https://example.com/news/1", "https://example.com/news/2"])

        # Create an instance of the Class object with the mocked find_link function
        with patch.object(ML_stock, 'find_link', mock_find_link):
            obj = self.stock

            # Call the scrap_news_SET method with the mocked return value
            obj.news = []

            # Call the scrap_news_SET method with the mocked return value
            result = obj.scrap_news_SET("https://example.com", ['ABC'])

            # Check that the function returns the expected value
            self.assertEqual(result, True)

            # Check that self.news is not an empty list when self.load_data_news is called
            self.assertEqual(obj.news, [])


    def test_scrap_news_SET_old_news(self):
        # Mock the return value of the find_link function
        mock_find_link = MagicMock(return_value=["https://example.com/news/1", "https://example.com/news/2"])

        # Create an instance of the Class object with the mocked find_link function
        obj = self.stock
        with patch.object(obj, 'find_link', mock_find_link):
            # Mock the return value of the load_data_news function
            mock_load_data_news = MagicMock(return_value=[['2022-01-01', 'ABC', 'URL', 'Ticker']])

            # Create an instance of the Class object with the mocked load_data_news function
            with patch.object(obj, 'load_data_news', mock_load_data_news):
                # Call the scrap_news_SET method with the mocked return value
                obj.news = [('2022-01-01', 'ABC', 'URL', 'Ticker')]
                result = obj.scrap_news_SET("https://example.com", ['ABC'])

                # Check that the function returns the expected value
                self.assertEqual(result, True)

                # Check that self.news is not an empty list when self.load_data_news is called
                self.assertNotEqual(obj.news, [])


    def test_next_page_scrap_success(self):
        # simulate a case where scrap_news_SET returns True on the second iteration
        def mock_scrap_news_SET(url, stock):
            if url == 'https://www.kaohoon.com/latest-news/page/2':
                return True
            else:
                return False
        self.stock.scrap_news_SET = mock_scrap_news_SET

        # call the method with a mock stock value
        result = self.stock.next_page_scrap('mock_stock')

        # assert that the method returned True
        self.assertEqual(result, 'Stop')

    def test_News_SET100(self):
        # Mock the return value of the find_link function
        mock_next_page_scrap = MagicMock(return_value='Stop')

        # Create an instance of the Class object with the mocked find_link function
        with patch.object(ML_stock, 'next_page_scrap', mock_next_page_scrap):

            # Call the scrap_news_SET method with the mocked return value
            result = self.stock.News_SET100()

            # Check that the function returns the expected value
            self.assertTrue(result)


    def test_news_Nasdaq(self):
        # Call the method to test here
        result = self.stock.news_Nasdaq(0)
        # Check the output
        self.assertTrue(result)

    def test_news_Crypto(self):
        # Call the method to test here
        result = self.stock.news_Crypto(0)
        # Check the output
        self.assertTrue(result)
    
    def test_getcity_and_latlong_have(self):
        Testtext = "I've live in London then I go to Bangkok when I was 20 years old"
        # Call the method to test here
        result = self.stock.getcity_and_latlong(Testtext)
        # Check the output
        df = pd.DataFrame({'city': ['Bangkok','London'],'lat':[13.752494,51.507336],'long':[100.493509,-0.12765]})
        assert_frame_equal(result, df)

    def test_getcity_and_latlong_nothave(self):
        Testtext = "I've live in asdwasdwadwasdwasdwasdw"
        # Call the method to test here
        result = self.stock.getcity_and_latlong(Testtext)
        # Check the output
        df = pd.DataFrame({'city': [],'lat':[],'long':[]})
        assert_frame_equal(result, df)
    
    def test_get_poppulate_for_city_have(self):
        df = pd.DataFrame({'city': ['Bangkok','Bangkok','London'],'lat':[13.752494,13.752494,51.507336],'long':[100.493509,100.493509,-0.12765]})
        self.stock.place = df
        # Call the method to test here
        result = self.stock.get_poppulate_for_city()
        # Check the output
        for_test = pd.DataFrame({'city': ['Bangkok','London'],'lat':[13.752494,51.507336],'long':[100.493509,-0.12765],'population':[2,1]})
        assert_frame_equal(result, for_test)

    def test_get_poppulate_for_city_nothave(self):
        df = pd.DataFrame({'city': ['Bangkok','London'],'lat':[13.752494,51.507336],'long':[100.493509,-0.12765]})
        self.stock.place = df
        # Call the method to test here
        result = self.stock.get_poppulate_for_city()
        # Check the output
        for_test = pd.DataFrame({'city': ['Bangkok','London'],'lat':[13.752494,51.507336],'long':[100.493509,-0.12765],'population':[1,1]})
        assert_frame_equal(result, for_test)
    
    def test_trans_set100_1(self):
        df = pd.DataFrame({'Datetime': [datetime.datetime(2022, 1, 2)],'Ticker':['Test'],'Body':['สวัสดี']})
        mock_input = df
        # Set the expected value of the result
        for_test = pd.DataFrame({'Datetime': [datetime.datetime(2022, 1, 2)],'Ticker':['Test'],'Body':['hello']})
        # Call the method to test here
        result = self.stock.trans_set100(mock_input)
        assert_frame_equal(result, for_test)

    def test_trans_set100_2(self):
        df = pd.DataFrame({'Datetime': [datetime.datetime(2022, 1, 2)],'Ticker':['Test'],'Body':['']})
        mock_input = df
        # Set the expected value of the result
        for_test = pd.DataFrame()
        # Call the method to test here
        result = self.stock.trans_set100(mock_input)
        assert_frame_equal(result, for_test)

    @patch('pandas.read_sql')
    def test_update_place(self,mock_read_sql):
        # Define the mock return values
        mock_check_index = pd.DataFrame({'Index':['SET100']})
        mock_check_Dplace = pd.DataFrame({'Datetime':[datetime.datetime(2023, 3, 1)]})
        mock_get_news = pd.DataFrame({'Datetime': ['2023-03-02'], 'Ticker': ['AAPL'], 'Body': ['some news']})

        # Mock the return value of trans_set100 and get_latlong_for_all_content to simulate data processing
        mock_trans_set100 = MagicMock(return_value = pd.DataFrame({'Datetime': ['2022-03-02'], 'Ticker': ['ABC'], 'Body': ['some translated news']}))
        mock_get_latlong_for_all_content = MagicMock(return_value = pd.DataFrame({'city': ['Bangkok'], 'lat': [13.7563], 'long': [100.5018], 'Datetime': ['2022-03-02'], 'Ticker': ['ABC']}))
        for_test = pd.DataFrame({'city': ['Bangkok'], 'lat': [13.7563], 'long': [100.5018], 'Datetime': ['2022-03-02'], 'Ticker': ['ABC']})
        # Set the mock return values for the read_sql function
        mock_read_sql.side_effect = [
            mock_check_index,
            mock_check_Dplace,
            mock_get_news
        ]
        obj = self.stock
        with patch.object(obj, 'get_latlong_for_all_content', mock_get_latlong_for_all_content):
            # Mock the return value of the load_data_news function
            mock_get_latlong_for_all_content.return_value = pd.DataFrame({'city': ['Bangkok'], 'lat': [13.7563], 'long': [100.5018], 'Datetime': ['2022-03-02'], 'Ticker': ['ABC']})
            # call the code that uses my_function
            result = obj.update_place('AAPL')

            # assert that the result is as expected
            assert_frame_equal(result, for_test)

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
        x = datetime.datetime.now()
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
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        usd_markets = [market for market in markets if market.endswith('/USDT')]
        crypto_tickers = [market.replace('/','-').replace('USDT','USD') for market in usd_markets]
        nasdaq_tickers = pdr.nasdaq_trader.get_nasdaq_symbols().index.tolist()
        op = webdriver.ChromeOptions()
        op.add_argument('headless') 
        driver = webdriver.Chrome(options=op)
        df2 = pd.DataFrame()
        InsSec = []
        driver.get("https://finance.yahoo.com/quote/%s/profile?p=%s"% (Ticker,Ticker))
        numlink = driver.find_elements(By.XPATH, '//span[@class="Fw(600)"]')
        for i in numlink[:2]:
            InsSec.append(i.text)
        try:
            if Ticker in nasdaq_tickers:
                df1 = pd.DataFrame({'Ticker': [Ticker], 'Industry Group': [InsSec[0]], 'Sector': [InsSec[1]], 'Index': ['NASDAQ']})
                df1.to_sql('stock_info',con=conn,if_exists='append',index=False)
                return df1
            elif Ticker in crypto_tickers:
                df1 = pd.DataFrame({'Ticker': [Ticker], 'Industry Group': [InsSec[0]], 'Sector': [InsSec[1]], 'Index': ['CRYPTO100']})
                df1.to_sql('stock_info',con=conn,if_exists='append',index=False)
                return df1
        except:
            pass
        return False

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

    def download_year (self,ticker,save):
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

    def download_quarter (self,ticker,save):
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
    
    def update_quarter (self,ticker):
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
    
    def update_year (self,ticker):
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
        if a == False:
            return False
        b = self.download_stock(Ticker)
        c = self.download_year(Ticker,True)
        d = self.download_quarter(Ticker,True)
        # e = news_one_Nasdaq(Ticker) # <---- ยังไม่ได้ลอง
        # g = download_place(Ticker) # <---- ยังไม่ได้ลอง
    
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

# if __name__ == '__main__':
#     unittest.main(argv=['first-arg-is-ignored'], exit=False)

ticker = 'AOT.BK'
# text = "Im from Mars"
# df = pd.DataFrame({'city': ['Bangkok','Bangkok'],'lat':[13.752494,13.752494],'long':[100.493509,100.493509]})
# period = 'Day'
a = ML_stock()
# a.download_new_stock('META')
# print(a.All_change_stock('Day'))
# a.getLastDate('Hour','PTT.BK') 
# a.getDiffDay()
# a.check_stock('PTT.BK')
# a.update('Hour','PTT.BK')
# print('here')
# print(a.getcity_and_latlong(text))
a.updateAll()
# print(a.get_poppulate_for_city())
# a.getLastDate(period)
# a.getDiffDay()
# print(a.update(ticker,period))
# a.news_one_Nasdaq('ABNB')