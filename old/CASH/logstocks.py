#stocksave.py

import ystockquote
import csv
biglist = []
stocklist = []
prices = {}
outpiece = []

class Line(object):

    def __init__(self, date, stock, close, kno, w, h, e, n, rd, perc,last1,last2):
        self.date = date
        self.stock = stock
        if close != 'Close':
            self.close = float(close)
        elif close == 'Close':
            self.close = close
        self.kno = kno
        self.w = w
        self.h = h
        self.e = e
        self.n = n
        self.rd = rd
        self.perc = perc
        self.last1 = last1
        self.last2 = last2

def logstocks(desired_csv_file,output_file_name,writingstocklist,verbose=False,limit=None):
    
    with open(desired_csv_file,'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            
            biglist.append(Line(row[0],row[1],row[2],row[3],row[4],row[5],\
                                row[6],row[7],row[8],row[9],0,0))
            
    biglist.sort(key = lambda r: r.stock)
    for line in biglist:
        if line.stock not in stocklist:
            stocklist.append(line.stock)
    counter = 0
    for stock in stocklist:
        if verbose:
            if stock != 'Stock':
                print "Logging price for {}".format(stock)
        if writingstocklist:
            outpiece.append(stock)
        prices[stock] = ystockquote.get_price(stock)
        counter += 1
        if counter == limit:
            break
    a = prices.keys()
    if "Stock" in a:
        a.remove("Stock")
    a.sort()
    
    with open(output_file_name, 'w') as g:
        writer = csv.writer(g)
        if verbose:
            print "Writing {}'s stocks to {} in the CASH folder".format(desired_csv_file,output_file_name)
        for stock in a:
            if verbose:
                print "{} : {}".format(stock, prices[stock])
            writer.writerow([stock,str(prices[stock])])
        
    if writingstocklist:
        with open('stocklist.csv', 'w') as b:
            writer = csv.writer(b)
            writer.writerow(['stocklist'])
            for elem in outpiece:
                writer.writerow([elem])
'''
b = 'sp500recent.csv'
c = 'sp500currvals.csv'
d = 'IBDcurrvals.csv'
h = 'IBDtestrobert.csv'
f = 'allstockstest.csv'
g = 'allstockscurrvals.csv'
'''

#ACTION LINE
#logstocks(h,d,True,True,None)

