import unittest
from unittest.mock import patch,MagicMock
import sqlite3
import pandas as pd
import datetime
import yfinance as yf
from pandas.testing import assert_frame_equal
from jupyter_dash import JupyterDash
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

class ML_stock:
    def __init__(self,Company):
        self.last = []
        self.LastDate = []
        self.DiffDay = 0
        self.Company = Company

    def getLastDate(self,period):
        conn = sqlite3.connect("stock.sqlite")
        # Query last element of stock in database
        if period == 'Hour':query = "SELECT * FROM stock_table_hr WHERE `ticker` = '%s'" % self.Company
        elif period == 'Day':query = "SELECT * FROM stock_table_d WHERE `ticker` = '%s'" % self.Company
        elif period == 'Mount':query = "SELECT * FROM stock_table_mo WHERE `ticker` = '%s'" % self.Company
        query = "SELECT * FROM stock_table WHERE `ticker` = '%s'" % self.Company
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

class GUI(ML_stock):
    def __init__(self):
        self.test = []
        super().__init__()
    def app(self):
        app = JupyterDash(__name__)
        app.layout = html.Div(children=[
            html.Div([
                html.H1(children='Stock Radar',
                        style={
                            'textAlign': 'center',
                            }
                ),
                html.Div([
                    "Stock : ",
                    dcc.Input(id='ticker-input', value='', type='text'),
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
                html.Button('Show Table', id='show-table-button'),
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
                    figure=self.plot('','Hour')
                )],
                style={
                        'margin-right': 20,
                        'margin-left': 20
                }
            ),

            dcc.ConfirmDialog(
                id='popup',
                message='Not found that tickers',
                displayed=False,
            ),
            dcc.ConfirmDialog(
                id='popup_dl',
                message='Downloaded',
                displayed=False,
            ),
            dcc.ConfirmDialog(
                id='popup_fa',
                message='False to download for this ticker',
                displayed=False,
            ),
            html.Div(id='table-container'),
        ])
    
    def plot(ticker, interval):
        now = datetime.datetime.now()
        last_month = now + dateutil.relativedelta.relativedelta(months=-1)
        seven_month = now + dateutil.relativedelta.relativedelta(months=-7)
        ten_year = now + dateutil.relativedelta.relativedelta(years=-10)
        conn = sqlite3.connect("stock.sqlite")
        cur = conn.cursor()
        query1 = "select * from stock_table_hr where `ticker` == '%s' and datetime > '%s' and datetime < '%s'" % (ticker, last_month, now)
        query2 = "select * from stock_table_d where `ticker` == '%s' and datetime > '%s' and datetime < '%s'" % (ticker, seven_month, now)
        query3 = "select * from stock_table_mo where `ticker` == '%s' and datetime > '%s' and datetime < '%s'" % (ticker, ten_year, now)
        Hr = pd.read_sql(query1,conn)
        Day = pd.read_sql(query2,conn)
        Mo = pd.read_sql(query3,conn)
        #declare figure
        fig = go.Figure()
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.1, subplot_titles=('OHLC', 'Volume','MACD'), 
                    row_width=[0.2, 0.7, 0.7])

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

        fig.update_xaxes(rangemode="nonnegative")
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(hovermode = "x")
        fig.update(layout_xaxis_rangeslider_visible=False)
        return fig
    
    def RPqt(self):
        url = 'http://127.0.0.1:8050/'

        app = QApplication(sys.argv)

        # QWebEngineView
        browser = QWebEngineView()
        browser.load(QUrl(url))
        browser.show()

        sys.exit(app.exec_())
    
    def getLastDate(self):
        super().getLastDate()

    def getDiffDay(self):
        super().getDiffDay()

    def update(self):
        super().update()

    
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
