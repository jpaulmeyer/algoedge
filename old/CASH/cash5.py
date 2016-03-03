#cash5.py

import ystockquote
import csv

##############
start_date = '3/30/1994' #default is 3/30/1994 (uses sp500recent)
end_date = '5/20/2015' #default is 5/20/2015 (uses sp500currvals)
##############


stocklines = []

truth = None
if end_date != '5/20/2015' or start_date != '3/30/1994':
    truth = 'giantunsorted.csv'
else:
    truth = 'sp500recent.csv'

g = 'sp500recent.csv'
truth = g
a = 'dadspfirst10.csv'
x = 'testaapl.csv'
z = 'IBDtestrobert.csv'
prices = {}#prices of stocks
cashes = []#cash I've had along the way
#Globals
biglist = []#list of Lines and StockLines
startingcash = 1.0
cash = startingcash
#superlist = [] #List of stocklists # stocklists are sorted by date
forbidden = [] #All dead stocks... yikes
from lineclass4 import *

def getstocksplitlines(): #Populates stocklines
    x = 'aaplsplits.csv'
    c = 'sp500splitlines.csv'
    r = 'allsplitlines.csv'
    rr = 'IBDsplits.csv'
    with open(r,'rU') as p:
        reader = csv.reader(p)
        for row in reader:
            stocklines.append(SplitLine(row[0],row[1],row[2],row[3]))

def getcurrvals(): #get the current stock prices 
    #must be in same dir
    b = 'sp500currvals.csv'
    qq = 'IBDcurrvals.csv'
    bb = 'enddatevals.csv'
    if end_date == '5/20/2015':
        actual = b
    else:
        actual = bb
    with open(actual,'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == 'N/A':
                forbidden.append(row[0])
            prices[row[0]] = row[1]

def filterprices():
    global prices
    new_prices = {}
    y = prices.keys()
    for stock in y:
        if prices[stock] != 'N/A':
            new_prices[stock] = prices[stock]
    prices = new_prices

def filterbiglist():
    global biglist
    newbiglist = []
    for line in biglist:
        if line.stock in forbidden:
            continue
        else:
            newbiglist.append(line)
    biglist = newbiglist

def annualreturn(initial,final,years):
    return str((((float(final)/float(initial))**(1./years))-1)*100)[:6] + " %"

def analyze(desired_csv_file, cash, startdate, enddate, sellallatend=True):
    getcurrvals() #populates prices
    print "Got current prices of stocks successfully!"
    with open(desired_csv_file,'rU') as f:
        reader = csv.reader(f)
        live = False
        for row in reader:
            if live:
                biglist.append(Line(row[0],row[1],row[2],row[3],row[4],row[5],\
                                row[6],row[7],row[8],row[9],0,0))#row[10],row[11]))
            else:
                live = True
    getstocksplitlines() 
    for splitline in stocklines:
        biglist.append(splitline)
    filterbiglist()
    biglist.sort(key = lambda r: r.dateval)
    print "Master list successfully sorted by date and contains no dead stocks"
    
    #print "GONNNA WRITE BIGLIST TO BIGLIST.CSV"

    with open('biglist.csv', 'w') as c:
        writer = csv.writer(c)
        for row in biglist:
            if row.dateobj.meat == '0/0/0':
                continue
            elif isinstance(row,Line):
                writer.writerow([row.sig,row.dateobj.meat,row.stock,row.close,row.kno,row.w,row.h,row.e,row.n,row.rd,row.perc,row.last1,row.last2])
            elif isinstance(row,SplitLine):
                writer.writerow([row.sig,row.dateobj.meat,row.stock,row.splitfrom,row.splitto])
                continue
            
    print "Analyzing given biglist......."
    live = False
    start = Date(startdate).dateval
    end = Date(enddate).dateval
    for line in biglist:
        if line.dateobj.dateval > start:
            live = True
        if live:
            #print str(line.dateobj.dateval) + '    ' + line.dateobj.meat
            if isinstance(line,SplitLine):#IF its a stocksplit line - do it and continue
                line.dosplit()
                continue
            elif isinstance(line,Line):
                line.check()
        if line.dateobj.dateval > end:
            live = False
    print '\n-------\n'           
    
    print "Done analyzing!"
    print "Processing cashlog......."
    #process cashlog (in lineclass)

    with open('cashlog.csv', 'w') as h:
        writer = csv.writer(h)
        cashlog.sort(key = lambda r:r.stock)
        writer.writerow(['TYPE' , 'DATE' , 'STOCK', 'PRICE' , 'AMT' , '# OF SHARES' , '$ SPENT/MADE' , 'CASH AFTER' ])
        for row in cashlog:
            writer.writerow([row.addsub,row.dateobj.meat,row.stock,row.price,row.amt,row.numshares,row.cashspentmade,row.cashafter])

    cashlog.sort(key = lambda r : r.dateobj.dateval)
    for i in range(len(cashlog)):
        if cashlog[i].addsub == 'ADD':
            cash += cashlog[i].cashspentmade
        elif cashlog[i].addsub == 'SUB':
            cash -= cashlog[i].cashspentmade
        #print "{} : {}".format(cash,cashlog[i])
        if cash < 0.0:
            #print 'debt rn'
            pass
        cashes.append([cashlog[i].dateobj.meat,cash])
        #counter += 1

    #print "Final: {}".format(cash)
    print "Processed cashlog!"

    if sellallatend:
        filterprices()
        print "Selling out entire current portfolio........"
        stocks = mystocks.keys()
        stocks.sort()
        for stock in stocks:
            if mystocks[stock][0] > 0:
                cashes.append(['end',cash])
                cash += float(prices[stock])*float(mystocks[stock][0])
                mystocks[stock][0] = 0
                #print "Selling remaining shares in: {}".format(stock)
    #print "Outputting cashlog into cashlog.csv..."


    
    print "Outputting cash records... into cashes.csv"
    with open('cashes.csv', 'w') as gg:
        writer = csv.writer(gg)
        for row in cashes:
            writer.writerow(row)
    
    print "***********"
    
    startyear = int(startdate[-4:])
    endyear = int(enddate[-4:])
    yearselapsed = endyear - startyear
    mostinvested = min([a[1] for a in cashes])
    
    filler = annualreturn(-1*mostinvested, mostinvested + cash, yearselapsed)
    #filler2 = annualreturn(mostinvested, mostinvested + cash, yearselapsed)
    
    print "START: ${}\nFINISH: ${}\nPROFIT: ${}\n\n% MADE: {}".format(startingcash,cash,cash-startingcash,filler)
    print "***********"
    
    bought = mystocks.keys()
    bought.sort()
    with open('stocksbought.csv', 'w') as h:
        writer = csv.writer(h)
        writer.writerow(['boughtlist'])
        for elem in bought:
            writer.writerow([elem])
analyze(truth,cash,start_date,end_date,True)

intermediate = [a[1] for a in cashes] 
print "The lowest amount of cash you had was {}".format(min(intermediate))
print "\n"

print "finding first Line"
firstLine = biglist[0]
for line in biglist:
    if isinstance(line,Line):#IF its a stocksplit line - do it and continue
        firstLine = line
        break
print "First line's date was: {}".format(firstLine.dateobj.meat)
print "Last line's date was: {}".format(biglist[-1].dateobj.meat)





#print "*****\nI made {}\nin {} years\nwhile having at most {} invested in the market.\n*****".format(profit
#print len(biglist) - len(stocklines)
#args: file, starting cash, sell at end, #doing stock splits or nah


#def performance():


#cant tell if have enough money rn
