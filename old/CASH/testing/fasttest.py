'''
This file takes in a user entered file, transactions.csv
'''


import csv
mystocks = {} # KO : [ numshares  ,  currpos ]
initcash = 10000000.0
cash = initcash #10m
cashlog = [] # [ SUB/ADD/DNB/DNS/ERR , date , stock , price , amt, numshares , cashspent , newcash ]
position = 100000.0 #100k

def buy(date,stock,price1,amt1):
    global cash
    price = float(price1)
    amt = float(amt1)
    if cash < 0:
        print "overdrawn?!?!"
        cashlog.append(['ERR',date,stock,price,amt,0,0,cash])#
    elif cash == 0:
        print "no moneys :("
        cashlog.append(['DNB',date,stock,price,amt,0,0,cash])#
    elif position*amt > cash and cash > 0.0:
        shares = cash/price
        mystocks[stock] = [shares, cash/(amt*position)]
        print "just spent last of your money on {}".format(stock)
        cashlog.append(['SUB',date,stock,price,amt,shares,cash,0])
        cash = 0
    elif stock not in mystocks.keys() and amt*position <= cash:
        cashlog.append(['SUB',date,stock,price,amt,position*amt/price,position*amt,cash-position*amt])#pay the cash for it
        mystocks[stock] = [position*amt/price, amt]
        cash -= position*amt
    elif stock in mystocks.keys():
        curr = mystocks[stock][1]
        if amt <= curr:#keep position steady
            pass
        elif amt > curr:#buy more
            cashlog.append(['SUB', date,stock,price,amt,position*(amt-curr)/price,amt-curr,cash-(amt-curr)]) #pay for it
            mystocks[stock] = [position*amt/price, amt]#add the new shares
            cash -= position*(amt-curr)
    else:
        pass
        print "error buying {}".format(stock)#error

def sell(date,stock,price1,amt1):
    global cash
    price = float(price1)
    amt = float(amt1)
    if stock in mystocks.keys():#if you've ever bought it
        if mystocks[stock][1] > 0.0 and mystocks[stock][0] > 0.0: #if you currently own it
            curr = mystocks[stock][1]
            if amt >= curr and curr > 0:
                ###sell everything
                cashlog.append(['ADD', date,stock,price,amt,mystocks[stock][0],mystocks[stock][0]*price,cash+(mystocks[stock][0]*price)])
                cash += mystocks[stock][0]*price
                mystocks[stock][1] = 0.0#take out the shares
                mystocks[stock][0] = 0.0
            elif amt < curr:
                ###sell some
                new = curr - amt #new position
                diffshares = mystocks[stock][0]*amt
                newshares = mystocks[stock][0] - diffshares #newamt of shares
                mystocks[stock][0] = newshares
                mystocks[stock][1] = new
                cashlog.append(['ADD',date,stock,price,amt,diffshares,diffshares*price,cash+(diffshares*price)])
                cash += diffshares*price #make the cash for the difference
    elif stock not in mystocks.keys() or mystocks[stock][1] == 0.0:
        cashlog.append(['DNS',date,stock,price,amt,0,0,cash])

transactions = []

name = 'transactions.csv'

#transactions.csv -- 5 columns: BUY/SELL , DATE , STOCK , PRICE , POS
#also has these as headers!

def babytransactions():
    with open('transactions.csv','w') as r:
        writer = csv.writer(r)
        writer.writerow(['BUY/SELL' , 'DATE' , 'STOCK' , 'PRICE' , 'POS'])
        writer.writerow(['buy','1/1/00','KO',100.0,1.0])
        writer.writerow(['sell','1/1/01','KO',200.0,1.0])

def writecashlog(filenum=1):
    with open('testlog{}.csv'.format(str(filenum)), 'w') as h:
        writer = csv.writer(h)
        writer.writerow(['TYPE' , 'DATE' , 'STOCK', 'PRICE' , 'AMT' , '# OF SHARES' , '$ SPENT/MADE' , 'CASH AFTER' ])
        for row in cashlog:
            writer.writerow(row)
        writer.writerow([])
        writer.writerow(['FINAL CASH:','${}'.format(cash)])
        writer.writerow(['% GAIN:','{}%'.format((cash-initcash)/initcash*100)])

def run(file_name,basic=False,num=1):
    print "writing original transactions.csv"
    if basic:
        babytransactions()#comment out later#
    print "importing transactions"
    with open(file_name, 'rU') as v:
        reader = csv.reader(v)
        live = False
        for row in reader:
            if live:
                transactions.append([row[0],row[1],row[2],row[3],row[4]])
            else:
                live = True
    print "executing transactions"
    for trans in transactions:
        if trans[0] == 'buy':
            buy(trans[1],trans[2],trans[3],trans[4])
        elif trans[0] == 'sell':
            sell(trans[1],trans[2],trans[3],trans[4])
        else:
            print "must say 'buy' or 'sell' in the first column of transactions.csv"
    print "writing cashlog"
    writecashlog()
    print "******\nfinal cash: {}\nprofit: {}%".format(cash,(cash-initcash)/initcash*100)

run(name,False)
