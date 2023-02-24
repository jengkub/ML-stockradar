import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import unittest
from unittest.mock import patch, mock_open
import csv
import sqlite3
import datetime

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
        conn = sqlite3.connect("tutorial.db")
        cur = conn.cursor()
        query = "select * from stock_table where `ticker` == '%s'" % self.Company
        self.r_df = pd.read_sql(query,conn)
        self.Ind = self.r_df.tail(1).industryGroup.to_string().split()[1]
        self.sec = self.r_df.tail(1).sector.to_string().split()[1]
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
        data.to_sql('stock_table',con=conn,if_exists='append',index=True)
        return data

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

    
# if __name__ == '__main__':
#     unittest.main()
ticker = 'AOT.BK'
a = ML_stock(ticker)
a.getLastDate()
print(a.getDiffDay())
# a.update(ticker)