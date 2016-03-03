#cash6.py




##### ADDING IN A START AND END DATE PARAMETER : MAKE DEFAULT ARGS 1/1/94 and 5/20/15







import ystockquote
import csv

stocklines = []
g = 'sp500recent.csv'
a = 'test2014.csv'
x = 'testaapl.csv'
z = 'testabt.csv'
prices = {}#prices of stocks
cashes = []#cash I've had along the way
#Globals
biglist = []#list of Lines and StockLines
startingcash = 100000.0
cash = startingcash
#superlist = [] #List of stocklists # stocklists are sorted by date
forbidden = [] #All dead stocks... yikes
from lineclass4 import *

def getstocksplitlines(): #Populates stocklines
    x = 'aaplsplits.csv'
    c = 'sp500splitlines.csv'
    r = 'allsplitlines.csv'
    with open(r,'rU') as p:
        reader = csv.reader(p)
        for row in reader:
            stocklines.append(SplitLine(row[0],row[1],row[2],row[3]))

def getcurrvals(): #get the current stock prices 
    #must be in same dir
    b = 'sp500currvals.csv'
    with open(b,'rU') as f:
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

def analyze(desired_csv_file, cash, sellallatend=True):
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
    for line in biglist:
        if isinstance(line,SplitLine):#IF its a stocksplit line - do it and continue
            line.dosplit()
            continue
        elif isinstance(line,Line):
            line.check()
    
    print "Done analyzing!"
    print "Processing cashlog......."
    #process cashlog (in lineclass)

    with open('cashlog.csv', 'w') as h:
        writer = csv.writer(h)
        writer.writerow(['TYPE' , 'DATE' , 'STOCK', 'PRICE' , 'AMT' , '# OF SHARES' , '$ SPENT/MADE' , 'CASH AFTER' ])
        for row in cashlog:
            writer.writerow(row)

    
    for i in range(len(cashlog)):
        if cashlog[i][0] == 'ADD':
            cash += cashlog[i][6]
        elif cashlog[i][0] == 'SUB':
            cash -= cashlog[i][6]
        #print "{} : {}".format(cash,cashlog[i])
        if cash < 0.0:
            #print 'debt rn'
            pass
        cashes.append(cash)
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
                cashes.append(cash)
                cash += float(prices[stock])*float(mystocks[stock][0])
                mystocks[stock][0] = 0
                #print "Selling remaining shares in: {}".format(stock)
    #print "Outputting cashlog into cashlog.csv..."
    
    #print "Outputting cash records..."
    
    print "***********"
    print "START: ${}\nFINISH: ${}\nPROFIT: ${}\n% INCREASE: {}%".format(startingcash,cash,cash-startingcash,(cash-startingcash)/startingcash*100)
    print "***********"
    
    bought = mystocks.keys()
    bought.sort()
    with open('stocksbought.csv', 'w') as h:
        writer = csv.writer(h)
        writer.writerow(['boughtlist'])
        for elem in bought:
            writer.writerow([elem])
analyze(a,cash,True)
print "The lowest amount of cash you had was {}".format(min(cashes))
print "\n"

print "finding first Line"
firstLine = biglist[0]
for line in biglist:
    if isinstance(line,Line):#IF its a stocksplit line - do it and continue
        firstLine = line
        break
print "First line's date was: {}".format(firstLine.dateobj.meat)
print "Last line's date was: {}".format(biglist[-1].dateobj.meat)

#print len(biglist) - len(stocklines)

#args: file, starting cash, sell at end, #doing stock splits or nah



#cant tell if have enough money rn
