import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import unittest
import csv
import datetime

class StockTestcase(unittest.TestCase):
    # def testSave(self):
    #     pass

    def testInfo(self):
        test = ML_stock("NKE")
        result = test.info()
        assert result == {'zip': '97005-6453', 'sector': 'Consumer Cyclical', 'fullTimeEmployees': 79100, 'longBusinessSummary': "NIKE, Inc., together with its subsidiaries, designs, develops, markets, and sells men's, women's, and kids athletic footwear, apparel, equipment, and accessories worldwide. The company provides athletic and casual footwear, apparel, and accessories under the Jumpman trademark; and casual sneakers, apparel, and accessories under the Converse, Chuck Taylor, All Star, One Star, Star Chevron, and Jack Purcell trademarks. In addition, it sells a line of performance equipment and accessories comprising bags, socks, sport balls, eyewear, timepieces, digital devices, bats, gloves, protective equipment, and other equipment for sports activities under the NIKE brand; and various plastic products to other manufacturers. The company markets apparel with licensed college and professional team, and league logos, as well as sells sports apparel. Additionally, it licenses unaffiliated parties to manufacture and sell apparel, digital devices, and applications and other equipment for sports activities under NIKE-owned trademarks. The company sells its products to footwear stores; sporting goods stores; athletic specialty stores; department stores; skate, tennis, and golf shops; and other retail accounts through NIKE-owned retail stores, digital platforms, independent distributors, licensees, and sales representatives. The company was formerly known as Blue Ribbon Sports, Inc. and changed its name to NIKE, Inc. in 1971. NIKE, Inc. was founded in 1964 and is headquartered in Beaverton, Oregon.", 'city': 'Beaverton', 'phone': '503 671 6453', 'state': 'OR', 'country': 'United States', 'companyOfficers': [], 'website': 'https://investors.nike.com', 'maxAge': 1, 'address1': 'One Bowerman Drive', 'industry': 'Footwear & Accessories', 'ebitdaMargins': 0.14616999, 'profitMargins': 0.11472999, 'grossMargins': 0.44588003, 'operatingCashflow': None, 'revenueGrowth': 0.172, 'operatingMargins': 0.1299, 'ebitda': 7177999872, 'targetLowPrice': 78, 'recommendationKey': 'buy', 'grossProfits': 21479000000, 'freeCashflow': None, 'targetMedianPrice': 130, 'currentPrice': 117.86, 'earningsGrowth': 0.024, 'currentRatio': 2.691, 'returnOnAssets': 0.10149, 'numberOfAnalystOpinions': 33, 'targetMeanPrice': 125.03, 'debtToEquity': 82.013, 'returnOnEquity': 0.37316, 'targetHighPrice': 185, 'totalCash': 10620999680, 'totalDebt': 12524999680, 'totalRevenue': 49107001344, 'totalCashPerShare': 6.813, 'financialCurrency': 'USD', 'revenuePerShare': 31.293, 'quickRatio': 1.574, 'recommendationMean': 2.2, 'exchange': 'NYQ', 'shortName': 'Nike, Inc.', 'longName': 'NIKE, Inc.', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '-18000000', 'quoteType': 'EQUITY', 'symbol': 'NKE', 'messageBoardId': 'finmb_291981', 'market': 'us_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 3.729, 'beta3Year': None, 'enterpriseToEbitda': 25.514, '52WeekChange': -0.30146617, 'morningStarRiskRating': None, 'forwardEps': 3.99, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 1259689984, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'totalAssets': None, 'bookValue': 9.796, 'sharesShort': 16188464, 'sharesPercentSharesOut': 0.010299999, 'fundFamily': None, 'lastFiscalYearEnd': 1653955200, 'heldPercentInstitutions': 0.82812, 'netIncomeToCommon': 5633999872, 'trailingEps': 3.54, 'lastDividendValue': 0.34, 'SandP52WeekChange': -0.19671148, 'priceToBook': 12.031442, 'heldPercentInsiders': 0.012410001, 'nextFiscalYearEnd': 1717113600, 'yield': None, 'mostRecentQuarter': 1669766400, 'shortRatio': 2.17, 'sharesShortPreviousMonthDate': 1667174400, 'floatShares': 1238968480, 'beta': 1.144755, 'enterpriseValue': 183137746944, 'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': 1450915200, 'lastSplitFactor': '2:1', 'legalType': None, 'lastDividendDate': 1669939200, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': -0.004, 'priceToSalesTrailing12Months': 3.755118, 'dateShortInterest': 1669766400, 'pegRatio': 5.49, 'ytdReturn': None, 'forwardPE': 29.538847, 'lastCapGain': None, 'shortPercentOfFloat': 0.0165, 'sharesShortPriorMonth': 17377903, 'impliedSharesOutstanding': 0, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 116.25, 'regularMarketOpen': 116.47, 'twoHundredDayAverage': 110.25765, 'trailingAnnualDividendYield': 0.0107956985, 'payoutRatio': 0.3545, 'volume24Hr': None, 'regularMarketDayHigh': 118.1983, 'navPrice': None, 'averageDailyVolume10Day': 12848320, 'regularMarketPreviousClose': 116.25, 'fiftyDayAverage': 101.6324, 'trailingAnnualDividendRate': 1.255, 'open': 116.47, 'toCurrency': None, 'averageVolume10days': 12848320, 'expireDate': None, 'algorithm': None, 'dividendRate': 1.36, 'exDividendDate': 1669939200, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 115.82, 'currency': 'USD', 'trailingPE': 33.293785, 'regularMarketVolume': 2947715, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 184402575360, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 9827469, 'dayLow': 115.82, 'ask': 117.93, 'askSize': 900, 'volume': 2947715, 'fiftyTwoWeekHigh': 170.12, 'fromCurrency': None, 'fiveYearAvgDividendYield': 0.95, 'fiftyTwoWeekLow': 82.22, 'bid': 117.99, 'tradeable': False, 'dividendYield': 0.0117, 'bidSize': 800, 'dayHigh': 118.1983, 'coinMarketCapLink': None, 'regularMarketPrice': 117.86, 'preMarketPrice': 116.4, 'logo_url': 'https://logo.clearbit.com/investors.nike.com', 'trailingPegRatio': 4.0266}


class ML_stock:
    def __init__(self,Company):
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

    def getDiffDay(self,ticker):
        with open("test.csv",'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[7] == ticker:
                    last = row
        x = datetime.datetime.now()
        DayMo365 = {'1':31,'2':28,'3':31,'4':30,'5':31,'6':30,'7':31,'8':31,'9':30,'10':31,'11':30,'12':31}
        self.LastDate = last[0].split()[0].split('-')
        DiffMo = int(x.month) - int(self.LastDate[1])
        DiffYe = int(x.year) - int(self.LastDate[0])
        if DiffYe == 0:
            if DiffMo == 0:
                DiffDay = int(x.day) - int(self.LastDate[2])
                if DiffDay != 0:
                    self.DiffDay = str(DiffDay) + 'd'
            elif DiffMo != 0 :
                for u in range(DiffMo):
                    DayM = DayM + DayMo365[str(int(self.LastDate[1])+count)]
                    count += 1
                DiffDay = DayM - int(self.LastDate[2]) + int(x.day)
                self.DiffDay = str(DiffDay) + 'd'
        elif DiffYe != 0:
            dayly = 0
            dayn = 0
            for j in range(1,int(self.LastDate[1])):
                dayly = dayly + DayMo365[str(j)]
            for i in range(1,int(x.month)):
                dayn = dayn + DayMo365[str(i)]
            DiffDay = (365*DiffYe) - dayly + dayn - int(self.LastDate[2]) + int(x.day)
            self.DiffDay = str(DiffDay) + 'd'
        return DiffDay
        
    def update(self,ticker):
        data = yf.download(tickers=ticker, period=self.DiffDay, interval='1h')
        for i in data.index.day:
            if data.index.year[count] == int(self.LastDate[0]):
                if data.index.month[count] == int(self.LastDate[1]):
                    if i == int(self.LastDate[2])+1:
                        break
            count += 1

        data['ticker'] = 'NKE'
        data = data.iloc[count:,:]
        data
        data.to_csv('test.csv',mode='a',header=False)

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

a = ML_stock('NKE')
print(a.getDiffDay('NKE'))