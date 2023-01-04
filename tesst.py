import unittest
import sqlite3
import pandas as pd
import datetime
import yfinance as yf

class TestMLStock(unittest.TestCase):
    def setUp(self):
        # Set up a sample stock table in a test sqlite database
        conn = sqlite3.connect("test.sqlite")
        cur = conn.cursor()
        cur.execute("CREATE TABLE stock_table (ticker text, Datetime text, open real, high real, low real, close real, volume real, industryGroup text, sector text)")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 10:00:00', 145.0, 146.5, 144.5, 146.0, 100000, 'Technology', 'Information Technology')")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 11:00:00', 146.0, 147.0, 145.5, 146.5, 120000, 'Technology', 'Information Technology')")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 12:00:00', 146.5, 147.0, 146.0, 146.5, 130000, 'Technology', 'Information Technology')")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 14:00:00', 146.5, 147.0, 146.0, 146.5, 140000, 'Technology', 'Information Technology')")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 15:00:00', 146.5, 147.0, 146.0, 146.5, 150000, 'Technology', 'Information Technology')")
        cur.execute("INSERT INTO stock_table VALUES ('AAPL', '2022-01-03 16:00:00', 146.5, 147.0, 146.0, 146.5, 160000, 'Technology', 'Information Technology')")
        conn.commit()
        conn.close()

        # Create an instance of the ML_stock class
        self.stock = ML_stock('AAPL')

    def test_gettable(self):
        # Test the gettable method to retrieve the stock data from the database
        self.stock.gettable()
        # Test that the returned dataframe is correct
        self.assertEqual(self.stock.r_df.ticker.tolist(), ['AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL', 'AAPL'])

    def test_getLastDate(self):
        # Test the getLastDate method to retrieve the last date in the stock data
        self.stock.getLastDate()
        # Test that the LastDate attribute is correct
        self.assertEqual(self.stock.LastDate, ['2022', '1', '3'])

    def test_getDiffDay(self):
        # Test the getDiffDay method to retrieve the number of days since the last date in the stock data
                # Set the current date to a fixed value for testing
        self.stock.LastDate = ['2022', '1', '1']
        diff_day = self.stock.getDiffDay()
        # Test that the DiffDay attribute is correct
        self.assertEqual(self.stock.DiffDay, '2d')
        
    def test_update(self):
        # Test the update method to retrieve new stock data from Yahoo Finance
        self.stock.update('AAPL')
        # Test that the new data has been added to the stock data in the database
        conn = sqlite3.connect("test.sqlite")
        cur = conn.cursor()
        query = "select * from stock_table where `ticker` == '%s'" % self.stock.Company
        r_df = pd.read_sql(query, conn)
        self.assertEqual(len(r_df), 7)

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

    def getLastDate(self):
        conn = sqlite3.connect("test.sqlite")
        cur = conn.cursor()
        query = "select * from stock_table where `ticker` == '%s'" % self.Company
        self.r_df = pd.read_sql(query,conn)
        self.Ind = self.r_df.tail(1).industryGroup.to_string().split()[1]
        self.sec = self.r_df.tail(1).sector.to_string().split()[1]
        last = self.r_df.tail(1).Datetime.to_string().split()
        self.LastDate = last[1].split()[0].split('-')
        cur.close()
        print(self.LastDate)

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
        
        
    def update(self,ticker):
        down = 0
        conn = sqlite3.connect("test.sqlite")
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
        data['industryGroup'] = self.Ind
        data['sector'] = self.sec
        data = data.iloc[count:,:]
        print(data)
        # data.to_sql('stock_table',con=conn,if_exists='append',index=True)

    def plot(self):
        data = yf.download(tickers=self.Company, period='1d', interval='1m')
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))

        fig.update_layout(
            title=self.Company,
            yaxis_title='Stock Price (USD per Shares)')

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig.show()


if __name__ == '__main__':
    unittest.main()

