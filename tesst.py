import unittest
from unittest.mock import patch,MagicMock
import sqlite3
import pandas as pd
import datetime
import yfinance as yf
from pandas.testing import assert_frame_equal

class TestMLStock(unittest.TestCase):
    def setUp(self):
        # Set up a sample stock table in a test sqlite database
        self.stock = ML_stock('ABC')

    @patch('sqlite3.connect')
    @patch('pandas.DataFrame.to_sql')
    def test_save_data_stock_forHR(self, mock_to_sql, mock_connect):
        # Create a sample DataFrame with some test data
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

        # Replace the real to_sql() method with the mock object
        mock_to_sql.return_value = None

        # Replace the real sqlite3.connect() method with the mock object
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # call the save_data_to_database function with some data
        self.stock.save_data_stock(df,'Hour')

        # Ensure that the connect() method was called with the correct database name
        mock_connect.assert_called_once_with('stock.sqlite')

        # Ensure that the to_sql() method was called with the correct table name and data
        expected_table = 'stock_table_hr'
        expected_if_exists = 'append'
        expected_index = True
        mock_to_sql.assert_called_once_with(expected_table, con=mock_conn, if_exists=expected_if_exists, index=expected_index)
    
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


class ML_stock:
    def __init__(self,Company):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.Company = Company

    
    def saveData(self,Date):
        df_list = list()
        for ticker in self.Company:
            data = yf.download(tickers=ticker, period=Date , interval='1h')
            data['ticker'] = ticker
            df_list.append(data)
        df = pd.concat(df_list)
        df.to_csv('data.csv')

    def info(self):
        data = yf.Ticker(self.Company)
        return data.info

    def gettable(self):
        conn = sqlite3.connect("test.sqlite")
        cur = conn.cursor()
        query = "select * from stock_table where `ticker` == '%s'" % self.Company
        r_df = pd.read_sql(query,conn)
        print(r_df)

    def save_data_to_database(self,data):
        # connect to the database
        conn = sqlite3.connect('test.sqlite')
        # create a cursor
        cursor = conn.cursor()
        # save the data to the database
        cursor.execute("INSERT INTO table_name (data) VALUES (?)", (data,))
        # commit the changes
        conn.commit()
        # close the connection
        conn.close()

    def save_data_stock(self,data,period):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        # save the data to the database
        if period == 'Hour':data.to_sql('stock_table_hr',con=conn,if_exists='append',index=True)
        elif period == 'Day':data.to_sql('stock_table_d',con=conn,if_exists='append',index=True)
        elif period == 'Mount':data.to_sql('stock_table_mo',con=conn,if_exists='append',index=True)
        # close the connection
        conn.close()

    def save_data_news(self,data):
        # connect to the database
        conn = sqlite3.connect('stock.sqlite')
        # save the data to the database
        data.to_sql('stock_news',con=conn,if_exists='append',index=False)
        # close the connection
        conn.close()

if __name__ == '__main__':
    unittest.main()

