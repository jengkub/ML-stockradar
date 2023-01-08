import unittest
from unittest.mock import patch,MagicMock
import sqlite3
import pandas as pd
import datetime
import yfinance as yf
from pandas.testing import assert_frame_equal

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
        result = self.stock.getLastDate('test.db')

        # Make assertions about the result
        self.assertEqual(result, ['2022', '01', '01'])
    
    @patch('datetime.datetime')
    def test_getDiffDay_sameDay(self, mock_datetime):
        #Set last date
        self.stock.LastDate = ['2022','01','01']
        # Set date time
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2022
        mock_now.mount = 1
        mock_now.day = 1

        # Call the method being tested
        result = self.stock.getDiffDay()

        # Make assertions about the result
        self.assertEqual(result, '0d')
        mock_datetime.now.assert_called_once()

    @patch('datetime.datetime')
    def test_getDiffDay_OneYear(self, mock_datetime):
        # Set last date
        self.stock.LastDate = ['2022','01','01']
        # Set date time
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2023
        mock_now.mount = 1
        mock_now.day = 1

        # Call the method to tested
        result = self.stock.getDiffDay()

        # assertions about the result
        self.assertEqual(result, '365d')
        # Check Datetime is called
        mock_datetime.now.assert_called_once()

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
        result = self.stock.update('ABC', mock_conn)
        mock_data.to_sql('stock_table', con=mock_conn, if_exists='append', index=True)
        # Make assertions about the result
        assert_frame_equal(result, mock_data)
        # self.assertTrue(result.equals(df))
        mock_download.assert_called_once_with(tickers='ABC', period=self.stock.DiffDay, interval='1h')
        mock_data.to_sql.assert_called_once_with('stock_table', con=mock_conn, if_exists='append', index=True)


class ML_stock:
    def __init__(self,Company):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.Company = Company

    def getLastDate(self, nameDB):
        conn = sqlite3.connect(nameDB)
        cur = conn.cursor()
        query = "SELECT * FROM stock_table WHERE `ticker` = '%s'" % self.Company
        self.r_df = pd.read_sql(query, conn)
        last = self.r_df.tail(1).Datetime.to_string().split()
        self.LastDate = last[1].split()[0].split('-')
        cur.close()
        print(self.LastDate)
        return self.LastDate

    def getDiffDay(self):
        x = datetime.datetime.now()
        count = 0
        DayM = 0
        DayMo365 = {'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
        DiffMo = int(x.month) - int(self.LastDate[1])
        DiffYe = int(x.year) - int(self.LastDate[0])
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
        
        
    def update(self,ticker,nameDB):
        down = 0
        count = 0
        conn = sqlite3.connect(nameDB)
        data = yf.download(tickers=ticker, period=self.DiffDay, interval='1h')
        print(self.DiffDay)
        for i in data.index.day:
            if data.index.year[count] == int(self.LastDate[0]):
                if data.index.month[count] == int(self.LastDate[1]):
                    if i == int(self.LastDate[2])+1:
                        break
            count += 1

        ok = self.r_df.tail(1).Datetime.to_string().split()[2]
        if ok == '10:00:00':
            down = 5
        elif ok == '11:00:00':
            down = 4
        elif ok == '12:00:00':
            down = 3
        elif ok == '14:00:00':
            down = 2
        elif ok == '15:00:00':
            down = 1
        elif ok == '16:00:00':
            down = 0

        count = count - down
        data['ticker'] = ticker
        data = data.iloc[count:,:]
        data.to_sql('stock_table',con=conn,if_exists='append',index=True)
        return data

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)