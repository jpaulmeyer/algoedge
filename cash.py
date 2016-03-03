#cash6.py

import csv
from datetime import date
from calendarplay import *
from stockuniverses import *
from strategies import *
from lookup import *
import plotly.plotly as py
#from plotly.graphobjs import *

mystocks = {}
cashlog = []
position = 100000.0
startingcash = 1.0
cash = startingcash

def sell(stock,amt):
    if self.stock in mystocks.keys():
        if mystocks[self.stock][1] > 0.0 and mystocks[self.stock][0] > 0.0:
            curr = mystocks[self.stock][1]
            if amt >= curr and curr > 0:
                cashlog.append(TransactionLine('ADD', Date(self.dateobj.meat), self.stock, self.close, amt, mystocks[self.stock][0], self.close*mystocks[self.stock][0],'x'))
                mystocks[self.stock][1] = 0.0
                mystocks[self.stock][0] = 0.0
            elif amt < curr:
                new = curr - amt
                diffshares = mystocks[self.stock][0]*(amt/curr)
                newshares = mystocks[self.stock][0] - diffshares
                mystocks[self.stock][0] = newshares
                mystocks[self.stock][1] = new
                cashlog.append(TransactionLine('ADD', Date(self.dateobj.meat), self.stock, self.close, amt, diffshares, self.close*diffshares,'x'))#make the cash for the difference
                
#cashlog: [ SUB/ADD , date , stock , price , amt, numshares , cash spent/made , newcash ('x')]
def buy(stock,amt):
    owned_stocks = portfolio.keys()
    if stock not in owned_stocks:
        cashlog.append(TransactionLine('SUB', Date(self.dateobj.meat), self.stock, self.close, amt, position*amt/self.close,position*amt,'x')) #pay the cash for it
        mystocks[self.stock] = [position*amt/self.close, amt] 
    elif self.stock in mystocks.keys():
        curr = mystocks[self.stock][1]
        if amt <= curr:
            pass
        elif amt > curr:
            cashlog.append(TransactionLine('SUB', Date(self.dateobj.meat), self.stock, self.close, amt, (amt-curr)*position/self.close, position*(amt-curr),'x')) #pay for it
            prevshares = mystocks[self.stock][0]
            mystocks[self.stock] = [prevshares + position*(amt-curr)/self.close, amt]#add the new shares
    else:
        print "error buying {}".format(self.stock)

def order(stock,amt):
    pass #implement later?

class TransactionLine(object):
    def __init__(self, addsub, dateobj, stock, price, amt, numshares, cashspentmade, cashafter):
        self.addsub = addsub
        self.date = dateobj
        self.stock = stock
        self.price = price
        self.amt = amt
        self.numshares = numshares
        self.cashspentmade = cashspentmade
        self.cashafter = cashafter

class SplitLine(object): 
    def __init__(self, datestring, stock, splitfrom, splitto):
        self.sig = 'split'
        self.date = date(int(datestring[:4]),int(datestring[-5:-3]),int(datestring[-2:]))
        self.stock = stock
        self.splitfrom = float(splitfrom)
        self.splitto = float(splitto)
        self.pricetoday = price_on_date(self.stock,self.date)
        self.seen = False

def getstocksplitlines():
    splitlines = []
    r = 'testsplitlines.csv'
    with open(r,'rU') as p:
        reader = csv.reader(p)
        for row in reader:
            splitlines.append(SplitLine(row[0],row[1],row[2],row[3]))
    return splitlines


startingcash = 10000000
'''
class Portfolio(object):
    def __init__(self,stocks={},amts={},cash=startingcash,assetval=0):
        self.stocks = stocks
        self.amts = amts
        self.cash = cash
        self.assetval = assetval

    def dosplit(self,split_obj):
        ratio = split_obj.splitto/split_obj.splitfrom
        if split_obj.stock in self.stocks.keys():
            self.stocks[split_obj.stock]*=ratio

    def buy(self,stock,amt):
        if stock in self.stocks.keys() and stock in self.amts.keys():
            #Figure out how much to actually buy
            oldamt = self.amts[stock]
            oldshares = self.stocks[stock]
            if amt > oldamt:
                diff = amt-oldamt
            elif amt <= oldamt:
                
            #Update self.amts and self.stocks to actually buy it
            
'''

def analyze(startdate, enddate, stockuniverse, strategy):
    splitlines = getstocksplitlines()
    dayspan = days_from_to(startdate,enddate)
    x_split = []
    x_sp500 = []
    x_inno = []
    y_split = []
    y_sp500 = []
    y_inno = []
    portfolio = Portfolio()
    for day in dayspan:
        nextsplitlines = splitlines
        x_sp500.append(day)
        y_sp500.append(price_on_date('SPY',day))
        for split in splitlines: # ^ Did a stock split happen today ^
            if split.date == day and (not split.seen):
                portfolio.dosplit(line)
                x_split.append(day)
                y_split.append(split.pricetoday)
                split.seen = True
                break 
        stocks_owned = portfolio.stocks.keys()
        for stock in stockuniverse:
            inno = innovest_on_date(stock,date)
            result = decide(inno,strategy) #'main' = strategy used=
            if result[0] == 'buy':
                buy(stock,result[1],portfolio)
            elif result[0] == 'sell':
                sell(stock,result[1],portfolio)
            #add to cashlog
        for stock in stocks_owned:
            pass
            #value portfolio
    trace0 = Scatter( #SP500 GRAPH
        x = x_sp500,
        y = y_sp500,
        mode = 'lines',
        name = 'SPY',
        line = Line(
            color = 'rgb(255,0,0)',
            width = 2
        )
    )
    trace1 = Scatter( #INNOVEST WORTH
        x = x_inno,
        y = y_inno,
        mode = 'lines',
        name = 'Innovest',
        line = Line(
            color = 'rgb(0,0,255)',
            width = 2
        )
    )
    data = Data([trace0,trace1])
    plot_url = py.plot(data, filename='Innovest vs SP500 ({})'.format(strategy))
        
autosetup = raw_input('AUTO SETUP y/n: ')
start = None
end = None
univ = None
strat = None
if autosetup == 'y':
    start = date(2000,1,1)
    end = date(2015,8,8)
    univ = 'testuniv'
    strat = 'main'
else:
    syear = raw_input('Start date? (Year): ')
    smonth = raw_input('Start date? (Month): ')
    sday = raw_input('Start date? (Day): ')

    eyear = raw_input('End date? (Year): ')
    emonth = raw_input('End date? (Month): ')
    eday = raw_input('End date? (Day): ')

    start = date(int(syear),int(smonth),int(sday))
    end = date(int(eyear),int(emonth),int(eday))

    univ = raw_input('Stock universe? (testuniv is default): ')
    strat = raw_input('Which strategy would you like to use: ')

######
analyze(start,end,getuniverse(univ),strat)
######


#SELL/BUY function takes in a portfolio object, returns a portfolio object
    



