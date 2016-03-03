#lineclass4.py

#The Line and Date Classes!

mystocks = {} #Stock : number of shares you own
cashlog = []
position = 100000.0


#OUTPUT Date, Stockname, .5/1.0/2.0, BUY/SELL, price 

class TransactionLine(object):

    def __init__(self, addsub, dateobj, stock, price, amt, numshares, cashspentmade, cashafter):
        self.addsub = addsub
        self.dateobj = dateobj
        self.stock = stock
        self.price = price
        self.amt = amt
        self.numshares = numshares
        self.cashspentmade = cashspentmade
        self.cashafter = cashafter

class Date(object):

    def __init__(self, datestring):
        self.sig = 'date'
        self.meat = datestring
        self.month = None
        self.day = None
        self.year = None
        current = ''
        counter = 1
        #processes datestring
        for i in range(len(self.meat)):
            if counter == 3:
                self.year = self.meat[i:len(self.meat)]
                break
            if self.meat[i] != '/':
                current += self.meat[i]
                continue
            elif self.meat[i] == '/':
                if counter == 1:
                    self.month = current
                elif counter == 2:
                    self.day = current
                current = ''
                counter += 1
        self.month = int(self.month)
        self.day = int(self.day)
        self.year = int(self.year)

        #assume everything is after 1940
        if self.year < 40 and self.year < 200:
            self.year += 2000
        elif self.year >= 40:
            self.year += 1900
        elif self.year > 100:
            self.year += 0
        self.dateval = 0 #days since day one sorta
        self.dateval += (self.year - 1940)*365.25
        self.dateval += self.month*31
        self.dateval += self.day
        ## fixes date thing 15 vs 2015 up to 2030
        if self.dateval > 32904:
            self.dateval -= 693975
        ##

        #self.dateval is what you sort on

class Line(object):

    def __init__(self, date, stock, close, kno, w, h, e, n, rd, perc,last1,last2):
        self.sig = 'line'
        if date != 'Date':
            self.dateobj = Date(date)
            self.dateval = self.dateobj.dateval
        elif date == 'Date':
            self.dateobj = Date('0/0/0')
            self.dateval = 0
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

    def sell(self,amt):
        if self.stock in mystocks.keys():#if you've ever bought it
            if mystocks[self.stock][1] > 0.0 and mystocks[self.stock][0] > 0.0: #if you currently own it
                curr = mystocks[self.stock][1]
                if amt >= curr and curr > 0:
                    ###sell everything
                    cashlog.append(TransactionLine('ADD', Date(self.dateobj.meat), self.stock, self.close, amt, mystocks[self.stock][0], self.close*mystocks[self.stock][0],'x'))
                    mystocks[self.stock][1] = 0.0#take out the shares
                    mystocks[self.stock][0] = 0.0
                elif amt < curr:
                    ###sell some
                    new = curr - amt #new position
                    diffshares = mystocks[self.stock][0]*(amt/curr)
                    newshares = mystocks[self.stock][0] - diffshares #newamt of shares
                    mystocks[self.stock][0] = newshares
                    mystocks[self.stock][1] = new
                    cashlog.append(TransactionLine('ADD', Date(self.dateobj.meat), self.stock, self.close, amt, diffshares, self.close*diffshares,'x'))#make the cash for the difference
                    
    #cashlog: [ SUB/ADD , date , stock , price , amt, numshares , cash spent/made , newcash ('x')]
    def buy(self,amt):
        if self.stock not in mystocks.keys(): #and self.close*amt*position <= cash:#have enough money, don't own it
            cashlog.append(TransactionLine('SUB', Date(self.dateobj.meat), self.stock, self.close, amt, position*amt/self.close,position*amt,'x')) #pay the cash for it
            mystocks[self.stock] = [position*amt/self.close, amt] #add the new shares in
        elif self.stock in mystocks.keys():#have enough money, own it
            curr = mystocks[self.stock][1]
            if amt <= curr:#keep position steady
                pass
            elif amt > curr:#buy more
                cashlog.append(TransactionLine('SUB', Date(self.dateobj.meat), self.stock, self.close, amt, (amt-curr)*position/self.close, position*(amt-curr),'x')) #pay for it
                prevshares = mystocks[self.stock][0]
                mystocks[self.stock] = [prevshares + position*(amt-curr)/self.close, amt]#add the new shares
                #position*(amt-curr)/self.close
        else:
            pass
            print "error buying {}".format(self.stock)#error

    def check(self): #original
        if self.kno[0:2] == '31':
            if self.perc == '83':
                self.buy(0.5)
            elif self.perc == '92':
                self.buy(1.0)
            elif self.perc == '100':
                self.buy(2.0)
        if self.kno[0:2] == '41':
            if self.perc == '83':
                self.sell(0.5)
            elif self.perc == '92':
                self.sell(1.0)
            elif self.perc == '100':
                self.sell(2.0)

    def check2(self):
        if self.kno[0:2] == '41':
            if self.perc == '83':
                self.buy(0.5)
            elif self.perc == '92':
                self.buy(1.0)
            elif self.perc == '100':
                self.buy(2.0)
        if self.kno[0:2] == '31':
            if self.perc == '92':
                self.sell(1.0)
            if self.perc == '100':
                self.sell(2.0)

class SplitLine(object): #Goes in as Date, Stock, From, To (so a 6 to 1 is FROM=1 TO=6)

    def __init__(self, dateline, stock, splitfrom, splitto):
        self.sig = 'split'
        a = Date(dateline)
        self.dateline = a.meat
        self.dateval = a.dateval
        self.dateobj = a
        self.stock = stock
        self.splitfrom = float(splitfrom)
        self.splitto = float(splitto)

    def dosplit(self):
        g = mystocks.keys()
        if self.stock in g and mystocks[self.stock][0] > .00001:
            q = mystocks[self.stock][0]
            multiplier = float(float(self.splitto)/float(self.splitfrom))
            mystocks[self.stock][0] *= multiplier
            #print "MULTI: {} ... {} for {} stocksplit for {}! Owned: {} shares, Now: {} shares!".format(multiplier,self.splitto,self.splitfrom,self.stock,q,mystocks[self.stock][0])









