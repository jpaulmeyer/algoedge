#price_on_date(ticker or sid, date(1,2,2000))

from datetime import date

class Inno(object):

    def __init__(date,ticker,kno,pct,price):
        self.date = date
        self.ticker = ticker
        self.kno = kno
        self.pct = pct
        self.price = price

def price_on_date(ticker,date): #return a price (float)
    print 'not implemented yet'

def innovest_on_date(ticker,date): #return a inno object!
    print 'not implemented yet'
